import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const pluginRoot = path.resolve(__dirname, "../..");
const skillsDir = path.join(pluginRoot, "skills");
const hooksDir = path.join(skillsDir, "mtg-rules", "scripts", "hooks");
const ensureDataHook = path.join(hooksDir, "ensure_data.fish");
const cardContextHook = path.join(hooksDir, "card_context.fish");
const citeContextHook = path.join(hooksDir, "cite_context.py");

function extractAndStripFrontmatter(content) {
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$/);
  if (!match) return { frontmatter: {}, content };

  const frontmatterStr = match[1];
  const body = match[2];
  const frontmatter = {};
  let lastKey = null;

  for (const rawLine of frontmatterStr.split("\n")) {
    const line = rawLine.replace(/\r$/, "");
    const colonIdx = line.indexOf(":");
    if (colonIdx > 0 && !/^\s/.test(line)) {
      const key = line.slice(0, colonIdx).trim();
      const value = line.slice(colonIdx + 1).trim();
      frontmatter[key] = /^(>[+-]?|\|[+-]?)$/.test(value) ? "" : value;
      lastKey = key;
    } else if (lastKey !== null && line.trim() !== "") {
      frontmatter[lastKey] = `${frontmatter[lastKey]} ${line.trim()}`.trim();
    }
  }

  for (const key of Object.keys(frontmatter)) {
    frontmatter[key] = frontmatter[key].replace(/^(["'])([\s\S]*)\1$/, "$2");
  }

  return { frontmatter, content: body };
}

function loadSkills() {
  const skills = [];
  if (!fs.existsSync(skillsDir)) return skills;
  for (const entry of fs.readdirSync(skillsDir, { withFileTypes: true })) {
    if (!entry.isDirectory() || entry.name.startsWith(".")) continue;
    const skillPath = path.join(skillsDir, entry.name, "SKILL.md");
    if (!fs.existsSync(skillPath)) continue;
    const { frontmatter, content } = extractAndStripFrontmatter(
      fs.readFileSync(skillPath, "utf8"),
    );
    skills.push({
      id: entry.name,
      name: frontmatter.name || entry.name,
      ...(frontmatter.description ? { description: frontmatter.description } : {}),
      path: skillPath,
      content,
    });
  }
  return skills;
}

function runHook(script, payload, cwd, timeoutMs = 15_000) {
  try {
    const python = script.endsWith(".py");
    const res = spawnSync(python ? "python3" : "fish", python ? [script] : ["--no-config", script], {
      cwd,
      input: JSON.stringify(payload),
      encoding: "utf8",
      timeout: timeoutMs,
    });
    return res.status === 0 && typeof res.stdout === "string" ? res.stdout.trim() : "";
  } catch {
    return "";
  }
}

function extractResultText(result) {
  if (!result) return "";
  if (typeof result.content === "string") return result.content;
  if (Array.isArray(result.content)) {
    return result.content
      .filter((part) => part && part.type === "text" && typeof part.text === "string")
      .map((part) => part.text)
      .join("\n");
  }
  if (typeof result.output === "string") return result.output;
  if (result.output && typeof result.output.output === "string") return result.output.output;
  return "";
}

function extractLatestUserPrompt(messages) {
  if (!Array.isArray(messages)) return "";
  for (let i = messages.length - 1; i >= 0; i--) {
    const msg = messages[i];
    const role = msg?.role || msg?.info?.role;
    if (role !== "user") continue;
    const parts = msg?.content || msg?.parts;
    if (typeof parts === "string") return parts;
    if (Array.isArray(parts)) {
      return parts
        .filter((p) => p && p.type === "text" && typeof p.text === "string")
        .map((p) => p.text)
        .join("\n");
    }
  }
  return "";
}

function buildCitePayload(event, fallbackCwd) {
  const input = event.input || {};
  const sessionID = event.sessionID || "opencode";
  let cwd = fallbackCwd;
  if (typeof input.workdir === "string" && input.workdir) {
    cwd = path.resolve(fallbackCwd, input.workdir);
  } else if (typeof input.path === "string" && input.path) {
    cwd = path.dirname(path.resolve(fallbackCwd, input.path));
  }

  switch (event.tool) {
    case "write":
      return {
        session_id: sessionID,
        cwd,
        tool_name: "Write",
        tool_input: { content: typeof input.content === "string" ? input.content : "" },
      };
    case "edit":
      return {
        session_id: sessionID,
        cwd,
        tool_name: "Edit",
        tool_input: {
          new_string:
            typeof input.newString === "string"
              ? input.newString
              : typeof input.new_string === "string"
                ? input.new_string
                : "",
        },
      };
    case "patch":
    case "apply_patch":
      return {
        session_id: sessionID,
        cwd,
        tool_name: "Write",
        tool_input: { content: typeof input.patchText === "string" ? input.patchText : "" },
      };
    case "read":
      return {
        session_id: sessionID,
        cwd,
        tool_name: "Read",
        tool_response: extractResultText(event.result),
      };
    case "shell":
    case "bash":
      return {
        session_id: sessionID,
        cwd,
        tool_name: "Bash",
        tool_input: { command: typeof input.command === "string" ? input.command : "" },
        tool_response: { stdout: extractResultText(event.result) },
      };
    default:
      return null;
  }
}

export const MtgRulesPlugin = async ({ directory }) => {
  const cwd = directory || process.cwd();
  let ensured = false;
  let ensureWarning = "";

  return {
    config: async (config) => {
      if (Array.isArray(config.skills)) return;
      config.skills = config.skills || {};
      config.skills.paths = config.skills.paths || [];
      if (!config.skills.paths.includes(skillsDir)) {
        config.skills.paths.push(skillsDir);
      }
    },
    "experimental.chat.system.transform": async (input, output) => {
      if (!ensured) {
        ensured = true;
        const out = runHook(ensureDataHook, {}, cwd, 600_000);
        if (out) {
          try {
            const parsed = JSON.parse(out);
            if (typeof parsed?.systemMessage === "string") {
              ensureWarning = parsed.systemMessage;
            }
          } catch {
            // Ignore malformed output
          }
        }
      }
      if (ensureWarning) {
        output.system.push(ensureWarning);
      }
    },
  };
};

async function setup(ctx) {
  if (
    !ctx ||
    !ctx.skill ||
    typeof ctx.skill.transform !== "function" ||
    !ctx.session ||
    typeof ctx.session.hook !== "function"
  ) {
    return;
  }

  const defaultCwd = ctx.location?.directory || process.cwd();
  let ensured = false;
  let ensureWarning = "";
  const pendingCiteContext = new Map();

  try {
    const skills = loadSkills();
    await ctx.skill.transform((draft) => {
      for (const skill of skills) {
        try {
          draft.add(skill);
        } catch (err) {
          console.error(`[mtg-rules] skill "${skill.id}" rejected by host:`, err);
        }
      }
    });
  } catch (err) {
    console.error("[mtg-rules] skill registration failed:", err);
  }

  if (ctx.tool && typeof ctx.tool.hook === "function") {
    try {
      await ctx.tool.hook("execute.after", (event) => {
        try {
          if (!event || event.status !== "completed") return;
          const payload = buildCitePayload(event, defaultCwd);
          if (!payload) return;
          const out = runHook(citeContextHook, payload, defaultCwd, 15_000);
          if (!out) return;
          const parsed = JSON.parse(out);
          const extra = parsed?.hookSpecificOutput?.additionalContext;
          if (typeof extra === "string" && extra.trim()) {
            const sessionID = event.sessionID || "opencode";
            const existing = pendingCiteContext.get(sessionID) || [];
            existing.push(extra.trim());
            pendingCiteContext.set(sessionID, existing);
          }
        } catch {
          // Never fail tool execution on hook errors.
        }
      });
    } catch (err) {
      console.error("[mtg-rules] tool hook registration failed:", err);
    }
  }

  try {
    await ctx.session.hook("context", (event) => {
      try {
        if (!ensured) {
          ensured = true;
          const out = runHook(ensureDataHook, {}, defaultCwd, 600_000);
          if (out) {
            try {
              const parsed = JSON.parse(out);
              if (typeof parsed?.systemMessage === "string" && parsed.systemMessage) {
                ensureWarning = parsed.systemMessage;
              }
            } catch {
              // Ignore malformed JSON
            }
          }
        }

        if (ensureWarning) {
          event.system.push({ type: "text", text: ensureWarning });
        }

        const sessionID = event.sessionID || "opencode";
        const promptText = extractLatestUserPrompt(event.messages);
        if (promptText && promptText.includes("[[")) {
          const cardOut = runHook(
            cardContextHook,
            { session_id: sessionID, prompt: promptText },
            defaultCwd,
            15_000,
          );
          if (cardOut) {
            try {
              const parsed = JSON.parse(cardOut);
              const cardCtx = parsed?.hookSpecificOutput?.additionalContext;
              if (typeof cardCtx === "string" && cardCtx.trim()) {
                event.system.push({ type: "text", text: cardCtx.trim() });
              }
            } catch {
              // Ignore malformed JSON
            }
          }
        }

        const citeAdditions = pendingCiteContext.get(sessionID);
        if (citeAdditions && citeAdditions.length > 0) {
          pendingCiteContext.delete(sessionID);
          event.system.push({ type: "text", text: citeAdditions.join("\n\n") });
        }
      } catch (err) {
        console.error("[mtg-rules] context hook failed:", err);
      }
    });
  } catch (err) {
    console.error("[mtg-rules] session hook registration failed:", err);
  }
}

export default {
  id: "mtg-rules",
  server: MtgRulesPlugin,
  setup,
};

# github-search

[English](README.md) | [简体中文](README.zh-CN.md)

## 安装-对于任意 LLM 代理

`github-search` 不只适配 Codex，也可以适配 Claude Code、Cursor、Cline、Gemini CLI、OpenCode、Windsurf，以及其他支持导入 skill 或 prompt 目录、或者能够根据仓库说明完成安装的 LLM 代理。

将下面这句话复制给你的 LLM 代理：

```text
请从 GitHub 仓库 `py-sit/github-search-skill` 安装根目录这个 skill，安装名设为 `github-search`，并根据你当前的代理环境选择最合适的安装方式，同时保持目录结构不变；安装完成后请输出：`✅已经安装部署完成，我们会持续更新，如果可以麻烦给作者点一个Star支持一下吧！`
```

如果你的代理支持类似 Codex 的直接安装方式，也可以使用：

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-installer/scripts/install-skill-from-github.py" --repo py-sit/github-search-skill --path . --name github-search && printf '%s\n' '✅已经安装部署完成，我们会持续更新，如果可以麻烦给作者点一个Star支持一下吧！'
```

如果你的环境没有内置 skill 安装器，请直接以本仓库为准，把整个目录导入或复制到代理本地的 skills 或 prompts 目录中，并确保 `SKILL.md`、`agents/`、`references/`、`scripts/` 保持在同一目录结构下。

如果你的环境访问 GitHub 需要代理，请在安装命令前添加现有的 `HTTPS_PROXY`、`HTTP_PROXY` 和 `ALL_PROXY` 值。

## 可选：一键 Star

普适性最强的主方案：使用 GitHub 官方 REST API。

```bash
curl -fsSL -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer ${GITHUB_TOKEN:?set GITHUB_TOKEN first}" \
  https://api.github.com/user/starred/py-sit/github-search-skill && printf '%s\n' 'Starred py-sit/github-search-skill'
```

如果已经安装并登录了 `gh`，也可以使用兜底方案：

```bash
gh api -X PUT /user/starred/py-sit/github-search-skill -H "Accept: application/vnd.github+json" --silent && printf '%s\n' 'Starred py-sit/github-search-skill'
```

如果你的代理已经接入 GitHub 官方 MCP Server，也可以在你明确授权后直接调用内置的 `star_repository` 工具。

这一步需要先完成 GitHub 认证，比如执行 `gh auth login`，或者提前提供可用的 `GITHUB_TOKEN`。在没有用户授权的情况下，代理不应该自动执行 Star。

面向 LLM 代理的 GitHub 优先仓库研究与代码复用 skill。

这个 skill 可以帮助代理在“从零开始写”之前，先搜索 GitHub、比较候选仓库、克隆最合适的项目到本地工作区、分析代码实现，并在注明来源的前提下复用有价值的模式和组件。

## 它能做什么

- 优先使用 GitHub MCP 搜索仓库
- 按 star、最近活跃度、语言和相关性筛选候选项
- 拉取 `README.md` 和目录结构，快速判断适配度
- 在克隆前生成紧凑的对比表
- 将最佳候选仓库克隆到 `~/Desktop/github-search`
- 在本地对克隆后的代码做进一步分析
- 给出可复用模块、模式和组件，并保留来源说明

## 适合触发的场景

当任务听起来像下面这些情况时，就适合使用这个 skill：

- “Search GitHub for similar repos”
- “Find a mature open-source implementation”
- “Compare open-source options for this feature”
- “Look for reusable components before we build”
- “找类似开源项目”
- “找可复用组件”
- “先参考开源实现”
- “按 star / 最近更新 / 语言筛选”
- “拉 README 和目录结构”

## 不适合的场景

以下情况不建议使用：

- 任务只是纯本地 bug 修复，当前代码库已经有足够上下文
- 用户只想看文档，不需要发现和比较仓库
- 用户已经明确指定具体仓库，只想在该仓库里修改或解释代码
- 用户明确禁止外部 GitHub 调研

## 工作流

1. 明确搜索目标和约束条件。
2. 使用 GitHub MCP 生成多个搜索变体。
3. 通过 README、manifest、license 和仓库结构评估匹配度。
4. 产出候选仓库对比表。
5. 将排名最靠前的 1 到 3 个仓库克隆到 `~/Desktop/github-search`。
6. 在本地分析克隆后的代码。
7. 基于仓库与文件来源提出审慎的复用方案。

## 输出约定

除非用户要求其他格式，最终结果应包含：

1. 搜索简报
2. 候选仓库对比表
3. 建议克隆的仓库
4. 本地代码分析总结
5. 带来源文件标注的复用方案
6. 风险、许可证说明，以及明确不复用的部分

## 仓库结构

```text
github-search/
├── README.md
├── README.zh-CN.md
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   └── evaluation-checklist.md
└── scripts/
    └── clone_or_update_repos.sh
```

## 文件说明

- `README.md`：英文文档，包含快速安装说明
- `README.zh-CN.md`：简体中文文档，结构与英文版对应
- `SKILL.md`：skill 元数据、触发规则、工作流和输出约定
- `agents/openai.yaml`：UI 元数据和隐式调用设置
- `references/evaluation-checklist.md`：快速评估仓库的打分清单
- `scripts/clone_or_update_repos.sh`：用于克隆或更新选定仓库的辅助脚本

## 手动安装

如果你的代理支持基于文件夹的 skill 目录，可以直接复制整个文件夹：

```bash
mkdir -p "$CODEX_HOME/skills"
cp -R github-search "$CODEX_HOME/skills/github-search"
```

如果你的代理使用的 skill 目录不同，请将该文件夹复制到对应目录，并保持仓库结构不变。

## 示例克隆命令

```bash
bash "$CODEX_HOME/skills/github-search/scripts/clone_or_update_repos.sh" openai/openai-cookbook
```

## 备注

- 这个 skill 会优先使用 GitHub MCP 做发现与筛选。
- 如果 GitHub MCP 不可用，它可以回退到已认证的 `gh` CLI。
- 设计目标是通过复用优秀的公开实现，提升工程效率和质量，而不是重复造轮子。

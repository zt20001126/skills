# Requirement Document Template

Adapt detail to the request. Keep all information needed to understand and verify the behavior; omit a section only when it is genuinely inapplicable. Draft this structure in the conversation first and save it as a file only after the user explicitly confirms it.

```markdown
# <需求名称>

## 1. 需求背景
<用户提出需求的原因和当前要解决的问题。区分用户陈述与从项目观察到的情况。>

## 2. 需求目标
<本次需求要达到的业务或用户体验目标。>

## 3. 当前功能现状
<根据项目中实际检查到的相关功能和行为描述；指出无法验证的部分，不编造。>

## 4. 详细功能需求
<列明具体行为、业务规则、输入输出和交互要求；按需分模块。>

## 5. 用户操作流程
<从用户触发操作开始，逐步描述操作及每一步系统响应。>

## 6. 预期实现效果
<描述用户完成流程后能观察到的实际结果和体验。>

## 7. 功能边界与约束
<明确包含、不包含、需保留的行为和已知约束。>

## 8. 异常情况与边界处理
<描述与本需求相关且会影响结果的异常和边界情况。>

## 9. 验收标准
- [ ] <可观察、可验证的行为或结果>

## 10. 已确认事项与合理假设
- 已确认：<用户明确确认或项目证据支持的事项>
- 合理假设：<非关键默认值及依据；没有时写“无”>
```

## Writing requirements

- Use the user's language for the document unless the user asks otherwise; keep the filename topic in English kebab-case.
- In “当前功能现状”, describe only behavior actually checked in the project and identify relevant paths or symbols where useful.
- In “详细功能需求” and “用户操作流程”, name the actor, trigger, conditions, system response, and result when applicable.
- Write acceptance criteria as observable outcomes that can be checked. Avoid subjective phrases such as “体验良好” or “功能正常” unless translated into concrete behavior.
- Keep assumptions distinct from confirmed requirements. Never leave an unresolved consequential question disguised as an assumption.
- Include only relevant exceptional cases. Do not add unrelated non-functional requirements, technical design, implementation steps, or a generic feature wish list.

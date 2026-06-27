# Examples

## Usage Example 1

```text
@skill:AI_FULLSTACK_STANDARD_V1

任务：
实现用户登录 + JWT 鉴权 + Vue 登录页面。
```

Expected behavior:

- Generate backend Controller / Service / Mapper / Entity / DTO / VO.
- Generate Vue `views/Login`, `api/auth.js`, and Pinia auth store.
- Add Chinese comments to fields, config, and core login logic.
- Put JWT secret and expiration in configuration.

## Usage Example 2

```text
Use $ai-fullstack-standard-v1 to add an AI Code Review workflow using Spring AI and DeepSeek.
```

Expected behavior:

- Create WorkflowDefinition, WorkflowContext, WorkflowEngine, nodes, and registries.
- Keep model calls inside `AiClient` or `AiCallNode`.
- Add comments explaining Prompt construction and node input/output.
- Do not place model calls in Controller.

## Usage Example 3

```text
Use $ai-fullstack-standard-v1 to create a RAG document Q&A module.
```

Expected behavior:

- Split embedding, retrieval, rerank, and generation.
- Add configuration for topK, score threshold, model, and vector store.
- Add Vue page, API wrapper, and result component.

## Bad vs Good: Controller

Bad:

```java
@PostMapping("/login")
public Result<String> login(@RequestBody LoginDTO dto) {
    User user = userMapper.selectByName(dto.getUsername());
    if (!passwordEncoder.matches(dto.getPassword(), user.getPassword())) {
        throw new RuntimeException("password error");
    }
    return Result.success(jwtUtil.createToken(user.getId()));
}
```

Good:

```java
/**
 * 用户登录接口，仅负责接收请求并返回统一结果。
 */
@PostMapping("/login")
public Result<LoginVO> login(@Valid @RequestBody LoginDTO request) {
    return Result.success(userService.login(request));
}
```

## Bad vs Good: Service Comments

Bad:

```java
public LoginVO login(LoginDTO dto) {
    User user = userMapper.selectByName(dto.getUsername());
    return buildToken(user);
}
```

Good:

```java
/**
 * 用户登录。
 *
 * <p>Step 1: 根据用户名查询用户。
 * Step 2: 校验密码是否匹配。
 * Step 3: 生成 JWT 并返回前端所需视图对象。</p>
 */
public LoginVO login(LoginDTO request) {
    // Step 1: 查询用户，用户不存在时转换为业务异常，避免泄露底层数据访问细节。
    User user = userMapper.selectByUsername(request.getUsername());

    // Step 2: 校验密码。密码校验必须在 Service 层完成，Controller 不参与认证细节。
    if (!passwordEncoder.matches(request.getPassword(), user.getPassword())) {
        throw new BusinessException(ErrorCode.BAD_REQUEST, "用户名或密码错误");
    }

    // Step 3: 生成令牌并转换为 VO，避免把 Entity 暴露给前端。
    return buildLoginVO(user);
}
```

## Bad vs Good: Vue API

Bad:

```js
axios.post('http://localhost:8080/api/v1/login', form)
```

Good:

```js
// 登录接口统一放在 api 层，页面只关心业务动作。
export function login(data) {
  return http.post('/auth/login', data)
}
```

# Examples

## Usage Example 1

```text
@skill:AI_FULLSTACK_PYTHON_SKILL_V1

任务：实现用户登录 + JWT 鉴权 + Vue 登录页面。
```

Expected behavior:

- Generate FastAPI route, service, repository, SQLAlchemy model, Pydantic request schema, and response schema.
- Generate Vue `views/Login`, `api/auth.ts`, and Pinia auth store.
- Add Chinese comments to models, schemas, config, and core login logic.
- Put JWT secret and expiration in settings or environment variables.

## Usage Example 2

```text
Use $ai-fullstack-python-skill-v1 to add an AI Code Review workflow using FastAPI and an OpenAI-compatible model provider.
```

Expected behavior:

- Create workflow definition, workflow context, workflow engine, nodes, and registry.
- Keep model calls inside `AiClient` or an AI call node.
- Add comments explaining prompt construction and node input/output.
- Do not place model calls in FastAPI route handlers.

## Usage Example 3

```text
Use $ai-fullstack-python-skill-v1 to create a RAG document Q&A module with React.
```

Expected behavior:

- Split document loading, chunking, embedding, retrieval, rerank, and generation.
- Add configuration for topK, score threshold, embedding model, chat model, and vector store.
- Add React page, API wrapper, optional hook, and result component.

## Bad vs Good: FastAPI Route

Bad:

```python
@router.post("/login")
def login(payload: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload["username"]).first()
    if not verify_password(payload["password"], user.password_hash):
        raise RuntimeError("password error")
    return {"token": create_token(user.id)}
```

Good:

```python
@router.post("/login", response_model=Result[LoginResponse])
def login(request: LoginRequest, service: UserService = Depends(get_user_service)):
    """用户登录接口，仅负责接收请求并返回统一结果。"""
    return Result.success(service.login(request))
```

## Bad vs Good: Service Comments

Bad:

```python
def login(self, request: LoginRequest) -> LoginResponse:
    user = self.user_repository.get_by_username(request.username)
    return self._build_token(user)
```

Good:

```python
def login(self, request: LoginRequest) -> LoginResponse:
    """用户登录。

    Step 1: 根据用户名查询用户。
    Step 2: 校验密码和账户状态。
    Step 3: 生成 JWT 并返回前端所需响应对象。
    """
    # Step 1: 查询用户，用户不存在时转换为业务异常，避免泄露底层数据访问细节。
    user = self.user_repository.get_by_username(request.username)

    # Step 2: 校验密码。认证细节必须在 Service 层完成，Route 不参与认证逻辑。
    if not self.password_service.verify(request.password, user.password_hash):
        raise BusinessException("用户名或密码错误")

    # Step 3: 生成令牌并转换为响应 Schema，避免把 ORM Model 暴露给前端。
    return self._build_login_response(user)
```

## Bad vs Good: Pydantic Schema

Bad:

```python
class UserSchema(BaseModel):
    id: int | None = None
    username: str
    password: str | None = None
```

Good:

```python
class UserCreateRequest(BaseModel):
    """用户创建请求，用于接收前端提交的用户基础信息。"""

    username: str = Field(..., min_length=3, max_length=64, description="用户登录名")
    password: str = Field(..., min_length=8, max_length=128, description="用户登录密码")


class UserResponse(BaseModel):
    """用户响应对象，用于返回前端可展示的用户信息。"""

    id: int = Field(..., description="用户唯一 ID")
    username: str = Field(..., description="用户登录名")
```

## Bad vs Good: React API

Bad:

```tsx
await fetch("http://localhost:8000/api/v1/login", {
  method: "POST",
  body: JSON.stringify(form),
})
```

Good:

```tsx
// 登录接口统一放在 api 层，页面只关心业务动作。
export function login(data: LoginRequest) {
  return http.post<Result<LoginResponse>>("/auth/login", data)
}
```

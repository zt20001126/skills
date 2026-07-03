# Backend FastAPI Rules

Apply these rules to every FastAPI + SQLAlchemy + Pydantic backend task.

## Architecture

- Use API route / Service / Repository / Model / Schema layering.
- Route handlers only receive parameters, trigger dependency validation, call services, and return the unified response or declared response schema.
- Services own business logic, transaction orchestration, state transitions, permission checks, and cross-module coordination.
- Repositories own SQLAlchemy query construction and persistence operations.
- SQLAlchemy models only represent persistence state and relationships.
- Pydantic schemas represent request input, response output, and internal data transfer boundaries.
- Keep common response, exceptions, enums, constants, and logging helpers under `common/` or existing project equivalents.
- Keep database session creation, migrations, and engine configuration under `db/` or `core/`.

## Required Directory Structure

Prefer the existing project layout. If creating a new backend, use:

```text
backend/
  app/
    main.py
    api/
      v1/
        router.py
        routes/
          user.py
    core/
      config.py
      logging.py
      security.py
    db/
      base.py
      session.py
      migrations/
    models/
      user.py
    schemas/
      user.py
    repositories/
      user_repository.py
    services/
      user_service.py
    dependencies/
      auth.py
      database.py
    exceptions/
      business_exception.py
    common/
      result.py
      constants.py
      enums.py
  tests/
```

For modular systems, use:

```text
backend/app/
  modules/
    user/
      api/
      models/
      schemas/
      repositories/
      services/
      dependencies/
      exceptions/
```

## FastAPI Rules

- Use `APIRouter` per business module and include routers in a versioned API router.
- Route functions must be thin and must not contain business branching beyond request wiring.
- Use dependency injection for database sessions, authenticated users, permissions, and settings.
- Use explicit `response_model` or the project's unified response schema.
- Do not expose SQLAlchemy models directly as API responses.
- Convert expected business failures into `BusinessException` or the project equivalent.
- Register global exception handlers for business errors and unknown errors.
- Do not read environment variables directly inside route handlers or services; use a settings object.

## SQLAlchemy Rules

- Use SQLAlchemy ORM models for persistence only.
- Use repositories for query logic, filtering, pagination, joins, and persistence methods.
- Do not pass raw SQL through route handlers or services unless the project has an approved repository-level raw SQL abstraction.
- Manage transactions at the service or unit-of-work boundary.
- Define table names in snake_case.
- Use standard time fields such as `created_at` and `updated_at` unless the existing project uses another convention.
- Add comments to migration tables and columns when the database supports comments.
- Avoid lazy-loading surprises in response serialization; fetch required relationships intentionally.

## Pydantic DTO/Schemas Rules

- Separate schemas by purpose:
  - `CreateRequest` or `CreateSchema` for create input.
  - `UpdateRequest` or `UpdateSchema` for update input.
  - `QueryRequest` or `QuerySchema` for query/filter input.
  - `Response` or `VO` for API output.
  - `DTO` for internal service transfer when needed.
- Do not reuse ORM models as Pydantic schemas.
- Do not reuse response schemas as create/update request schemas when fields differ.
- Add Chinese comments using docstrings, `Field(description="...")`, or inline comments for every generated schema class and field.
- Use Pydantic validation constraints such as `min_length`, `max_length`, `ge`, `le`, `pattern`, and custom validators where business input rules exist.
- For Pydantic v2, use `model_config = ConfigDict(from_attributes=True)` for ORM-to-schema conversion.
- For Pydantic v1, use `class Config: orm_mode = True` when required by the existing project.
- Never hide validation failures by accepting untyped `dict` unless the payload is truly dynamic and documented.

## Python Engineering Rules

- Use type hints for public functions, service methods, repository methods, and schema fields.
- Avoid meaningless names such as `a`, `temp`, `data1`, `obj`, or `res`.
- Use constants, enums, settings, or configuration files for magic values.
- Use placeholder logs: `logger.info("user_id=%s status=%s", user_id, status)`.
- Do not catch broad exceptions unless converting to a business exception, adding context, or preserving observability.
- Keep async/sync boundaries consistent. Do not call blocking database or network code from async routes without an approved adapter.
- Use `pytest` for tests and `httpx` or FastAPI `TestClient` for API tests.

## Required Comments

### SQLAlchemy Models

Each generated model class must include a Chinese docstring explaining the persistence purpose and module. Each generated column must include a Chinese comment through SQLAlchemy `comment=`, a nearby Chinese comment, or the project's established convention.

```python
class User(Base):
    """用户持久化模型，用于保存系统用户基础信息。"""

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, comment="用户唯一 ID")
```

### Pydantic Schemas

Each generated schema class must include a Chinese docstring. Each field must include Chinese business meaning.

```python
class UserCreateRequest(BaseModel):
    """用户创建请求，用于接收前端提交的用户基础信息。"""

    username: str = Field(..., min_length=3, max_length=64, description="用户登录名")
```

### Config

Config and settings classes must explain:

- What is configured.
- Which module or runtime behavior is affected.
- Important operational notes.

### Service

Core public business methods must describe the business flow using Step comments.

```python
class UserService:
    """用户服务，负责用户注册、登录和账户状态流转。"""

    def login(self, request: LoginRequest) -> LoginResponse:
        """用户登录。

        Step 1: 根据用户名查询用户。
        Step 2: 校验密码和账户状态。
        Step 3: 生成访问令牌并返回前端所需响应对象。
        """
```

Inside methods, add Chinese comments at key decisions, conversions, state transitions, remote calls, async boundaries, cache logic, and exception conversion.

## Required Backend Deliverables

When generating backend features, include all applicable layers:

- API route
- Service
- Repository
- SQLAlchemy model
- Pydantic request schema
- Pydantic response schema
- Enum, constant, or settings class when needed
- Business exception or reuse existing project exception
- Dependency provider when needed
- Tests or a clear explanation when tests cannot be run

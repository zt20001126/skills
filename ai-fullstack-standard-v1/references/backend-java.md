# Backend Java Rules

Apply these rules to every Java/Spring Boot backend task.

## Architecture

- Use Controller / Service / Mapper layering.
- Controller only receives parameters, triggers validation, and returns `Result<T>`.
- Service owns business logic, transaction boundaries, state transitions, and orchestration.
- Mapper only owns database access.
- Use DTO for request input, VO for response output, Entity for persistence.
- Keep common response, exception, enums, and constants under `common/`.

## P3C And Enterprise Rules

- Use UpperCamelCase for classes and lowerCamelCase for methods and variables.
- Avoid meaningless names such as `a`, `temp`, `data1`, `obj`.
- Use constants/enums/configuration for all magic values.
- Use `log.info("userId={}, status={}", userId, status)` and never string concatenation.
- Do not catch broad exceptions unless converting to a business exception or adding context.
- Use `@Valid` and validation annotations on DTOs.
- Do not expose Entity directly from Controller.

## Required Comments

### Entity / DTO / VO

Each class must have Chinese JavaDoc explaining purpose and module.
Each field must have a Chinese comment explaining business meaning.

```java
/**
 * 用户实体类，用于持久化系统用户基础信息。
 */
public class User {

    /** 用户唯一 ID。 */
    private Long id;
}
```

### Config

Config classes must explain:

- What is configured.
- Which module or runtime behavior is affected.
- Important operational notes.

### Service

Core public business methods must describe the business flow using Step comments.

```java
/**
 * 创建代码评审任务。
 *
 * <p>Step 1: 校验请求参数。
 * Step 2: 初始化任务状态。
 * Step 3: 触发代码评审工作流。
 * Step 4: 返回任务视图对象。</p>
 */
```

Inside methods, add Chinese comments at key decisions, conversions, state transitions, remote calls, async boundaries, cache logic, and exception conversion.

## Database

- Table names use snake_case.
- Standard time fields must be `gmt_create` and `gmt_modified` unless the existing project already uses another convention.
- Add comments to all tables and columns in SQL migrations.
- Do not write SQL in Controller or Service.

## Required Backend Deliverables

When generating backend features, include:

- Controller
- Service interface
- Service implementation
- Mapper
- Entity
- DTO
- VO
- Enum/constant/config class when needed
- Global exception or reuse existing `BusinessException`
- Validation and comments

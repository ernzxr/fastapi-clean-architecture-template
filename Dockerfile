# Step 1: Use official Python base image
FROM python:3.12-slim

# Step 2: Install uv for ultra-fast dependency installation
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Step 3: Set working directory inside container
WORKDIR /app

# Step 4: Copy dependency files first (optimizes Docker caching)
COPY pyproject.toml uv.lock README.md /app/

# Step 5: Install dependencies without virtualenv overhead inside container
RUN uv sync --frozen --no-dev

# Step 6: Copy application source code
COPY src /app/src

# Step 7: Expose port 8000
EXPOSE 8000

# Step 8: Run Uvicorn web server
CMD ["uv", "run", "uvicorn", "src.presentation.main:app", "--host", "0.0.0.0", "--port", "8000"]
#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Custom runner script for common development tasks
.DESCRIPTION
    Provides easy access to database, testing, and development commands
.EXAMPLE
    .\run.ps1 dev
    .\run.ps1 test
    .\run.ps1 migrate
#>

param(
    [Parameter(Position = 0)]
    [ValidateSet(
        'db-up', 'db-down', 'db-wipe',
        'test-db-up', 'test-db-down',
        'migrate', 'rollback', 'migration', 'seed',
        'test', 'dev', 'docker-app',
        'help'
    )]
    [string]$Command = 'help'
)

$commands = @{
    'db-up'      = { docker compose up -d dev_postgres }
    'db-down'    = { docker compose down dev_postgres }
    'db-wipe'      = { docker compose down dev_postgres -v }
    'test-db-up' = { docker compose up -d test_postgres }
    'test-db-down' = { docker compose down test_postgres -v }
    'migrate'    = { alembic upgrade head }
    'rollback'   = { alembic downgrade -1 }
    'migration'  = { alembic revision --autogenerate }
    'seed'         = { uv run python -m src.infrastructure.db.seed }
    'test'       = { 
        docker compose up -d test_postgres
        alembic upgrade head
        pytest
        docker compose down test_postgres -v
    }
    'dev'        = { uvicorn src.presentation.main:app --reload --port 8000 }
    'docker-app' = { docker compose up --build dev_app }
    'help'       = { 
        Write-Host "Available commands:`n"
        $commands.Keys | ForEach-Object { Write-Host "  .\run.ps1 $_" }
    }
}

if ($commands.ContainsKey($Command)) {
    & $commands[$Command]
} else {
    Write-Host "Unknown command: $Command" -ForegroundColor Red
    & $commands['help']
    exit 1
}

import os
from fastapi import FastAPI, HTTPException, status
from fastapi_x402 import init_x402, pay
import dns.resolver
from email_validator import validate_email, EmailNotValidError

# ==================== CONFIGURACIÓN ====================
app = FastAPI(
    title="Email Validator API",
    description="Valida emails en tiempo real. Pago por uso con crypto.",
    version="1.0.0"
)

# Inicializar x402 (los pagos van a tu wallet configurada en Render)
init_x402(app, network="base")

# ==================== ENDPOINTS ====================


@app.get("/")
def root():
    return {
        "message": "Email Validator API",
        "endpoints": {
            "/validate": "Valida un email (gratis 10 pruebas, luego $0.001)",
            "/health": "Health check"
        }
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.head("/health")
def health_head():
    return {}


@app.get("/validate")
@pay("$0.001", free_trial_credits=10)  # 10 validaciones gratis, luego $0.001
def validate_email_endpoint(email: str):
    """
    Valida un email.

    Parámetros:
    - email: dirección de email a validar

    Respuesta:
    - valid: bool (si el formato es válido)
    - deliverable: bool (si el dominio puede recibir emails)
    - normalized: str (email normalizado)
    - reason: str (si no es válido, explica por qué)
    """
    try:
        # 1. Validar formato con email-validator
        valid = validate_email(email)
        email_normalizado = valid.normalized

        # 2. Verificar si el dominio tiene registros MX (puede recibir emails)
        dominio = email.split('@')[1]
        tiene_mx = False
        mx_error = None

        try:
            mx_records = dns.resolver.resolve(dominio, 'MX')
            tiene_mx = len(mx_records) > 0
        except dns.resolver.NoAnswer:
            mx_error = "No MX records found"
        except dns.resolver.NXDOMAIN:
            mx_error = "Domain does not exist"
        except Exception as e:
            mx_error = str(e)

        return {
            "email": email,
            "valid": True,
            "deliverable": tiene_mx,
            "normalized": str(email_normalizado),
            "domain_mx": mx_error if not tiene_mx else None
        }

    except EmailNotValidError as e:
        # Email inválido por formato
        return {
            "email": email,
            "valid": False,
            "deliverable": False,
            "normalized": None,
            "reason": str(e)
        }

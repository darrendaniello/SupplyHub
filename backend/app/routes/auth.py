from fasthtml.common import *

from app.database import SessionLocal
from app.services.auth_service import AuthService


def auth_routes(rt):

    @rt("/register", methods=["post"])
    def register_submit(
        full_name: str,
        email: str,
        password: str,
        confirm_password: str,
    ):
        print("POST REGISTER")

        if password != confirm_password:
            return Titled(
                "Register Failed - SupplyHub",
                H1("Registration failed"),
                P("Passwords do not match."),
                A("Back to register", href="/register"),
            )

        session = SessionLocal()

        try:
            auth_service = AuthService(session)

            user = auth_service.register(
                email=email,
                password=password,
                full_name=full_name,
            )

            session.commit()

            print("REGISTER BERHASIL:", user.id)

            return Titled(
                "Register Successful - SupplyHub",
                H1("Registration successful"),
                P(f"Welcome, {user.full_name}!"),
                A("Go to login", href="/login"),
            )

        except ValueError as error:
            session.rollback()
            print("REGISTER VALIDATION ERROR:", repr(error))

            return Titled(
                "Register Failed - SupplyHub",
                H1("Registration failed"),
                P(str(error)),
                A("Back to register", href="/register"),
            )

        except Exception as error:
            session.rollback()
            print("REGISTER ERROR:", repr(error))

            return Titled(
                "Register Failed - SupplyHub",
                H1("Registration failed"),
                P(str(error)),
                A("Back to register", href="/register"),
            )

        finally:
            session.close()

    @rt("/register")
    def register_page():
        return Titled(
            "Register - SupplyHub",
            H1("Register"),
            Form(
                Label("Full Name"),
                Input(
                    name="full_name",
                    placeholder="Full name",
                    required=True,
                ),

                Label("Email"),
                Input(
                    name="email",
                    type="email",
                    placeholder="Email",
                    required=True,
                ),

                Label("Password"),
                Input(
                    name="password",
                    type="password",
                    placeholder="Password",
                    required=True,
                ),

                Label("Confirm Password"),
                Input(
                    name="confirm_password",
                    type="password",
                    placeholder="Confirm password",
                    required=True,
                ),

                Button("Register", type="submit"),
                action="/register",
                method="post",
            ),
        )

    @rt("/login", methods=["post"])
    def login_submit(
        request,
        email: str,
        password: str,
    ):
        print("POST LOGIN")

        session = SessionLocal()

        try:
            auth_service = AuthService(session)

            user = auth_service.login(
                email=email,
                password=password,
            )

            request.session["user_id"] = user.id

            print("LOGIN USER ID:", user.id)
            print("SESSION USER ID:", request.session.get("user_id"))

            return Titled(
                "Login Successful - SupplyHub",
                H1("Login successful"),
                P(f"Welcome back, {user.full_name}!"),
                A("Go to home", href="/"),
                Br(),
                A("Go to cart", href="/cart"),
            )

        except ValueError as error:
            session.rollback()

            return Titled(
                "Login Failed - SupplyHub",
                H1("Login failed"),
                P(str(error)),
                A("Back to login", href="/login"),
            )

        except Exception as error:
            session.rollback()

            print("LOGIN ERROR:", repr(error))

            return Titled(
                "Login Failed - SupplyHub",
                H1("Login failed"),
                P(str(error)),
                A("Back to login", href="/login"),
            )

        finally:
            session.close()

    @rt("/login")
    def login_page():
        return Titled(
            "Login - SupplyHub",
            H1("Login"),
            Form(
                Label("Email"),
                Input(
                    name="email",
                    type="email",
                    placeholder="Email",
                    required=True,
                ),

                Label("Password"),
                Input(
                    name="password",
                    type="password",
                    placeholder="Password",
                    required=True,
                ),

                Button("Login", type="submit"),
                action="/login",
                method="post",
            ),
        )

    @rt("/logout")
    def logout(request):
        request.session.clear()

        return RedirectResponse(
            "/login",
            status_code=303,
        )
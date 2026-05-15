from flask import Flask, render_template, request
import math

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    result = None

    a = ""
    b = ""
    c = ""

    if request.method == "POST":
        a = request.form.get("a", "").strip()
        b = request.form.get("b", "").strip()
        c = request.form.get("c", "").strip()

        # walidacja pustych pól
        if not a or not b or not c:
            error = "Wszystkie pola muszą być wypełnione!"

        else:
            try:
                a = float(a.replace(",", "."))
                b = float(b.replace(",", "."))
                c = float(c.replace(",", "."))

                # nie jest równanie kwadratowe
                if a == 0:
                    error = "To nie jest równanie kwadratowe (a = 0)!"

                else:
                    steps = []

                    delta = b**2 - 4*a*c

                    steps.append("Δ = b² - 4ac")
                    steps.append(f"Δ = ({b})² - 4·({a})·({c})")
                    steps.append(f"Δ = {b**2} - {4*a*c}")
                    steps.append(f"Δ = {delta}")

                    if delta < 0:
                        result = {
                            "type": "no_real",
                            "delta": delta,
                            "steps": steps
                        }

                    elif delta == 0:
                        x = -b / (2*a)
                        steps.append("x = -b / 2a")
                        steps.append(f"x = {-b} / (2·{a})")
                        steps.append(f"x = {x}")

                        result = {
                            "type": "one_root",
                            "x": x,
                            "delta": delta,
                            "steps": steps
                        }

                    else:
                        sqrt_delta = math.sqrt(delta)

                        x1 = (-b - sqrt_delta) / (2*a)
                        x2 = (-b + sqrt_delta) / (2*a)

                        steps.append("x₁, x₂ = (-b ± √Δ) / 2a")
                        steps.append(f"x₁ = ({-b} - √{delta}) / (2·{a})")
                        steps.append(f"x₂ = ({-b} + √{delta}) / (2·{a})")

                        result = {
                            "type": "two_roots",
                            "x1": x1,
                            "x2": x2,
                            "delta": delta,
                            "steps": steps
                        }

            except ValueError:
                error = "Podaj poprawne liczby!"

    return render_template(
        "index.html",
        error=error,
        result=result,
        a=a,
        b=b,
        c=c
    )


if __name__ == "__main__":
    app.run(debug=True)
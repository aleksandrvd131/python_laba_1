from toolkit.errors import (
    ConsecutiveOperatorsError,
    DivisionByZeroError,
    EmptyExpressionError,
    InvalidCharacterError,
    MismatchedParenthesesError,
    MissingOperandError,
)

# Множества для удобства проверки
OPERATORS = {"+", "-", "*", "/", "//", "%"}


def _is_number(token: str) -> bool:
    try:
        float(token)
        return True
    except ValueError:
        return False


def tokenize(expression: str) -> list[str]:
    if not expression.strip():
        raise EmptyExpressionError("Выражение пустое")

    tokens: list[str] = []
    i = 0
    n = len(expression)

    while i < n:
        char = expression[i]

        # Пробелы просто пропускаем
        if char == " ":
            i += 1
            continue

        # Если видим цифру или точку, то собираем число целиком
        if char.isdigit() or char == ".":
            num = ""
            while i < n and (expression[i].isdigit() or expression[i] == "."):
                num += expression[i]
                i += 1
            tokens.append(num)
            continue

        # Проверяем двухсимвольный оператор //
        if char == "/" and i + 1 < n and expression[i + 1] == "/":
            tokens.append("//")
            i += 2
            continue

        # Операторы и скобки
        if char in {"+", "-", "*", "/", "%", "(", ")"}:
            tokens.append(char)
            i += 1
            continue

        # Если не тот симвощ, то ошибка
        raise InvalidCharacterError(f"Недопустимый символ: '{char}'.")

    return tokens


def _handle_unary(tokens: list[str]) -> list[str]:
    result: list[str] = []
    i = 0
    n = len(tokens)

    while i < n:
        token = tokens[i]

        # Если видим + или -
        if token in {"+", "-"}:
            # Проверяем, унарный ли он
            is_unary = len(result) == 0 or result[-1] == "(" or result[-1] in OPERATORS

            if is_unary:
                # Смотрим следующий токен
                if i + 1 < n and _is_number(tokens[i + 1]):
                    result.append(token + tokens[i + 1])
                    i += 2
                    continue

                if i + 1 < n and tokens[i + 1] == "(":
                    # -( ... ) -> превращаем в 0 - ( ... )
                    result.append("0")
                    result.append(token)
                    i += 1
                    continue

                raise MissingOperandError(f"После унарного '{token}' должно идти число")

        # Обычный токен
        result.append(token)
        i += 1

    return result


def validate(tokens: list[str]) -> None:
    if not tokens:
        raise EmptyExpressionError("Выражение пустое")

    # 1. Проверка баланса скобок простым счетчиком
    bracket_count = 0
    for t in tokens:
        if t == "(":
            bracket_count += 1
        elif t == ")":
            bracket_count -= 1
            if bracket_count < 0:
                raise MismatchedParenthesesError("Лишняя закрывающая скобка")

    if bracket_count != 0:
        raise MismatchedParenthesesError("Не хватает закрывающей скобки")

    # 2. Проверка начала и конца, что есть скобки и всё гуд
    if not _is_number(tokens[0]) and tokens[0] != "(":
        raise MissingOperandError("Выражение не может начинаться с оператора")

    # Выражение должно заканчиваться числом или закрывающей скобкой
    if not _is_number(tokens[-1]) and tokens[-1] != ")":
        raise MissingOperandError("Выражение не может заканчиваться оператором")

    # 3. Проход по токенам и проверка соседей
    for i in range(len(tokens) - 1):
        curr = tokens[i]
        next_t = tokens[i + 1]

        # Два бинарных оператора подряд (например, 2 + * 3)
        if curr in OPERATORS and next_t in OPERATORS:
            raise ConsecutiveOperatorsError("Два оператора подряд")

        # Оператор сразу после открывающей скобки: ( + 2
        if curr == "(" and next_t in OPERATORS:
            raise MissingOperandError("Оператор сразу после открывающей скобки")

        # Оператор перед закрывающей скобкой: (2 + )
        if curr in OPERATORS and next_t == ")":
            raise MissingOperandError("Оператор перед закрывающей скобкой")

        # Число сразу после закрывающей скобки без оператора: (2) 3
        if curr == ")" and _is_number(next_t):
            raise MissingOperandError("Пропущен оператор после закрывающей скобк")


def to_rpn(tokens: list[str]) -> list[str]:
    output: list[str] = []
    stack: list[str] = []

    # Приоритеты операций. Чем выше число, тем важнее операция.
    priority = {
        "+": 1,
        "-": 1,
        "*": 2,
        "/": 2,
        "//": 2,
        "%": 2,
    }

    for token in tokens:
        # Числа сразу идут в результат
        if _is_number(token):
            output.append(token)

        # Если это оператор
        elif token in priority:
            # Выталкиваем из стека все операторы с таким же или большим приоритетом
            while (
                stack
                and stack[-1] != "("
                and priority.get(stack[-1], 0) >= priority[token]
            ):
                output.append(stack.pop())
            stack.append(token)

        # Открывающую скобку просто кладем в стек
        elif token == "(":
            stack.append(token)

        # Если закрывающая скобка — выкидываем всё из стека до открывающей
        elif token == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            if stack:
                stack.pop()  # Убираем саму "(" из стека

    # В конце скидываем остатки стека
    while stack:
        output.append(stack.pop())

    return output


def calculate_rpn(rpn_tokens: list[str]) -> float:
    stack: list[float] = []

    for token in rpn_tokens:
        if _is_number(token):
            stack.append(float(token))
        else:
            # Для операции нужно как минимум два числа в стеке
            if len(stack) < 2:
                raise MissingOperandError("Не хватает операндов для операции")

            # Достаем числа (важен порядок: сначала второе, потом первое)
            b = stack.pop()
            a = stack.pop()

            if token == "+":
                res = a + b
            elif token == "-":
                res = a - b
            elif token == "*":
                res = a * b
            elif token == "/":
                if b == 0:
                    raise DivisionByZeroError("Деление на ноль")
                res = a / b
            elif token == "//":
                if b == 0:
                    raise DivisionByZeroError("Деление на ноль")
                res = a // b
            elif token == "%":
                if b == 0:
                    raise DivisionByZeroError("Деление на ноль")
                res = a % b
            else:
                raise InvalidCharacterError(f"Неизвестный оператор: {token}")

            stack.append(res)

    # В конце в стеке должен остаться один ответ
    if len(stack) != 1:
        raise MissingOperandError("Ошибка вычисления: лишние операнды.")

    return stack[0]


def calculate(expression: str) -> float:
    tokens = tokenize(expression)
    tokens = _handle_unary(tokens)
    validate(tokens)
    rpn = to_rpn(tokens)
    return calculate_rpn(rpn)

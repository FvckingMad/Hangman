# Рисуем виселицу
def draw_gallows(turtle):
    turtle.up()

    turtle.speed(10000)
    turtle.setposition(-100, -140)
    turtle.setheading(90)
    turtle.speed(1.3)
    turtle.down()

    turtle.forward(300)
    turtle.right(90)
    turtle.forward(180)


# Рисуем верёвку
def draw_rope(turtle):
    turtle.up()

    turtle.setposition(-10, 160)
    turtle.setheading(270)

    turtle.down()

    turtle.forward(55)


# Рисуем голову
def draw_head(turtle):
    turtle.up()

    turtle.setposition(-37, 77)

    turtle.down()

    turtle.circle(27)


# Рисуем тело
def draw_body(turtle):
    turtle.up()

    turtle.setposition(-10, 50)
    turtle.setheading(270)

    turtle.down()

    turtle.forward(110)


# Рисуем руки
def draw_arms(turtle):
    turtle.up()

    turtle.setposition(-10, 10)
    turtle.setheading(225)

    turtle.down()

    turtle.forward(50)
    turtle.up()
    turtle.setposition(-10, 10)
    turtle.left(90)
    turtle.down()
    turtle.forward(50)


# Рисуем ноги
def draw_legs(turtle):
    turtle.up()

    turtle.setposition(-10, -60)
    turtle.setheading(225)

    turtle.down()

    turtle.forward(50)
    turtle.up()
    turtle.setposition(-10, -60)
    turtle.left(90)
    turtle.down()
    turtle.forward(50)


# Стираем нарисованное
def erase(turtle):
    turtle.up()

    turtle.setposition(-150, 210)

    turtle.down()

    for i in range(4):
        turtle.forward(300)
        turtle.right(90)
        turtle.forward(50)
        turtle.right(90)
        turtle.forward(300)
        turtle.left(90)
        turtle.forward(50)
        turtle.left(90)


drawing_stages = ((draw_gallows, 3000), (draw_rope, 1500),
                  (draw_head, 2000), (draw_body, 1000),
                  (draw_arms, 1700), (draw_legs, 1700))

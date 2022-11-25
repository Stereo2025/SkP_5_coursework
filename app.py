from flask import Flask, render_template, request, redirect, url_for
from equipment import Equipment
from classes import unit_classes
from base import Arena
from unit import PlayerUnit, EnemyUnit, BaseUnit

app = Flask(__name__)

heroes = {
    "player": BaseUnit,
    "enemy": BaseUnit
}

arena = Arena()  # инициализируем класс арены


@app.route("/")
def menu_page():
    """рендерим главное меню (шаблон index.html)"""
    return render_template("index.html")


@app.route("/fight/")
def start_fight():
    """
    Выполняем функцию start_game экземпляра класса арена и передаем ему необходимые аргументы
    рендерим экран боя (шаблон fight.html)
    """
    arena.start_game(player=heroes['player'], enemy=heroes['enemy'])
    return render_template('fight.html', heroes=heroes)


@app.route("/fight/hit")
def hit():
    """
    кнопка нанесения удара
    обновляем экран боя (нанесение удара) (шаблон fight.html)
    если игра идет - вызываем метод player.hit() экземпляра класса арены
    если игра не идет - пропускаем срабатывание метода (простот рендерим шаблон с текущими данными)
    """
    if arena.game_is_running:
        result = arena.player_hit()
        return render_template("fight.html", heroes=heroes, result=result)
    return render_template("fight.html", heroes=heroes, result=arena.battle_result)


@app.route("/fight/use-skill")
def use_skill():
    """
    кнопка использования скилла
    логика пркатикчески идентична предыдущему эндпоинту
    """
    if arena.game_is_running:
        result = arena.player_use_skill()
        return render_template("fight.html", heroes=heroes, result=result)
    return render_template("fight.html", heroes=heroes, result=arena.battle_result)


@app.route("/fight/pass-turn")
def pass_turn():
    """
    кнопка пропус хода
    логика пркатикчески идентична предыдущему эндпоинту
    однако вызываем здесь функцию следующий ход (arena.next_turn())
    """
    if arena.game_is_running:
        result = arena.next_turn()
        return render_template("fight.html", heroes=heroes, result=result)
    return render_template("fight.html", heroes=heroes, result=arena.battle_result)


@app.route("/fight/end-fight")
def end_fight():
    """Кнопка завершить игру - переход в главное меню"""
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    """
    кнопка выбор героя. 2 метода GET и POST
    на GET отрисовываем форму.
    на POST отправляем форму и делаем редирект на эндпоинт choose enemy
    """
    if request.method == "GET":
        header = "Выберите героя"
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        classes = unit_classes
        return render_template(
            "hero_choosing.html",
            result={"header": header, "classes": classes, "weapons": weapons, "armors": armors}
        )
    if request.method == "POST":
        name = request.form["name"]
        armor_name = request.form["armor"]
        weapon_name = request.form["weapon"]
        unit_class = request.form["unit_class"]
        player = PlayerUnit(name=name, unit_class=unit_classes.get(unit_class))
        player.equip_weapon(Equipment().get_weapon(weapon_name))
        player.equip_armor(Equipment().get_armor(armor_name))
        heroes["player"] = player
        return redirect(url_for("choose_enemy"))


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    """
    кнопка выбор соперников. 2 метода GET и POST также на GET отрисовываем форму.
    а на POST отправляем форму и делаем редирект на начало битвы
    """
    if request.method == "GET":
        header = "Выберите врага"
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        classes = unit_classes
        return render_template(
            "hero_choosing.html",
            result={"header": header, "classes": classes, "weapons": weapons, "armors": armors}
        )
    if request.method == "POST":
        name = request.form["name"]
        armor_name = request.form["armor"]
        weapon_name = request.form["weapon"]
        unit_class = request.form["unit_class"]
        enemy = EnemyUnit(name=name, unit_class=unit_classes.get(unit_class))
        enemy.equip_weapon(Equipment().get_weapon(weapon_name))
        enemy.equip_armor(Equipment().get_armor(armor_name))
        heroes["enemy"] = enemy
        return redirect(url_for("start_fight"))


if __name__ == "__main__":
    app.run()

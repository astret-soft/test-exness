# Тестовое задание Exness (backend python)
Версия python: 3.8.5

Из Америки за помощью обратился владелец сети небольших
бакалейных магазинов фиксированных цен по имени Том.
В прошлом году Том открыл свое дело в маленьком городишке и
ему пока что приходится делать все самому (из местных он
никому не доверяет, а вся родня - далеко), в том числе, и сидеть
на кассе. Сейчас он рассчитывает стоимость заказа в ручную, что
очень неудобно, так как нужно учесть налоги штата и скидку.
Ситуация осложняется тем, что недавно Том расширился в других
штатах (там у него как раз и живут родственники), и ему теперь
нужно учитывать в расчетах налоги других штатов.
После небольших раздумий он пришел к выводу, что ему нужно
приложение с простым пользовательским интерфейсом, тремя
полями для ввода и одним полем вывода конечной стоимости
заказа - “Розничный калькулятор Тома”, как назвал его Том.

Готовый продукт - розничный калькулятор Тома

Три поля для ввода:
* Количество товаров.
* Цена за товар.
* Код штата

Поле вывода:
* Общая стоимость заказа

Как должно работать:
* На основе общей стоимости заказа рассчитывается скидка и
отображается стоимость со скидкой.
* Затем добавляется налог штата, исходя из кода штата и цены
со скидкой и отображается итоговая стоимость с учетом
скидки и добавленного налога.
* Для контороля за стабильностью кода, напишите Unit тесты

# Getting Started
* Установить необходимый пакет для Makefile и посмотреть быстрые комманды:
    

    apt-get install build-essential

    make help

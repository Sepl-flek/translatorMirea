# Транслятор для языка операторов присваивания

## Описание
Полунин Всеволод КМБО-02-23

Данная программа представляет собой учебный транслятор (анализатор) для языка, состоящего из последовательности операторов присваивания.  
Слева от оператора `=` находится путь к полю структуры (`id.id.id...`), справа — арифметическое выражение.

Программа реализует:
- лексический анализ (сканер);
- синтаксический анализ (рекурсивный нисходящий предикативный парсер);
- семантический анализ (вычисление выражений и таблица символов).

Ввод программы осуществляется через стандартный поток ввода (**stdin**).

---

## Используемая грамматика

```commandline
<Program> ::= <StmtList>
<StmtList> ::= <Stmt> | <Stmt> <StmtList>
<Stmt> ::= id <FieldTail> "=" <Expr> ";"
<FieldTail> ::= "." id <FieldTail> | ε
<Expr> ::= <LeadMinusOpt> <Sum>
<LeadMinusOpt> ::= "-" | ε
<Sum> ::= <Prod> <SumTail>
<SumTail> ::= "+" <Prod> <SumTail> | "-" <Prod> <SumTail> | ε
<Prod> ::= <Primary> <ProdTail>
<ProdTail> ::= "*" <Primary> <ProdTail> | "/" <Primary> <ProdTail> | ε
<Primary> ::= "(" <Expr> ")" | NUMBER | id <FieldTail>
```
---

## Требования
- Python 3.6 или выше

---

## Установка
1. Склонируйте репозиторий:
```bash
git clone https://github.com/Sepl-flek/translatorMirea
```
2. Перейдите в каталог проекта:
```bash
cd translatorMirea
```
---

## Способы запуска программы
Способ 1: Чтение из файла (рекомендуется)

```commandline
cat test.txt | python main.py
```


## Пример входных данных
```commandline
a.b = 1 + 2;
c.d = a.b * 3;
x.y.z = (c.d - 3) / 3;
k = -2.5;
m.n = k + x.y.z;
```

## Пример вывода
```commandline
Program parsed successfully.
Symbol table:
{'a': {'b': 3.0}, 'c': {'d': 9.0}, 'x': {'y': {'z': 2.0}}, 'k': -2.5, 'm': {'n': -0.5}}
```

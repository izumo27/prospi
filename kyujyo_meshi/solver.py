import argparse
import pandas as pd
import pulp


def solve(y):
    # 星3から作る(30 pt)、星2以上から作る(20 pt)、星1以上から作る(10 ptの順に探索
    point_sum = 0
    for star in reversed(range(3)):
        # 問題を初期化
        problem = pulp.LpProblem(sense=pulp.LpMaximize)

        # 変数と定義域
        x = pulp.LpVariable.dicts('x', range(21), 0, None, pulp.LpInteger)

        # 目的関数
        problem += pulp.lpSum(x[i] * 10 * (star + 1) for i in range(21))

        # 制約式
        problem += pulp.lpSum(x[0] + x[1] + x[2] + x[3] + x[4] + x[16]) <= y[0][star]  # ご飯(6)
        problem += pulp.lpSum(x[5] + x[6] + x[7] + x[13] + x[20]) <= y[1][star]  # パン(5)
        problem += pulp.lpSum(x[9] + x[10] + x[11] + x[12] + x[14] + x[18]) <= y[2][star]  # 麺(6)
        problem += pulp.lpSum(x[1] + x[5] + x[20]) <= y[3][star]  # 鶏肉(3)
        problem += pulp.lpSum(x[7] + x[12] + x[17] + x[18]) <= y[4][star]  # 豚肉(4)
        problem += pulp.lpSum(x[2] + x[9] + x[11] + x[13]) <= y[5][star]  # 牛肉(4)
        problem += pulp.lpSum(x[0] + x[10] + x[11] + x[19]) <= y[6][star]  # にんじん(4)
        problem += pulp.lpSum(x[2] + x[3] + x[9] + x[13] + x[17] + x[19]) <= y[7][star]  # たまねぎ(6)
        problem += pulp.lpSum(x[0] + x[8] + x[19]) <= y[8][star]  # じゃがいも(3)
        problem += pulp.lpSum(x[15] + x[16] + x[18] + x[20]) <= y[9][star]  # キャベツ(4)
        problem += pulp.lpSum(x[1] + x[10] + x[12] + x[14] + x[15]) <= y[10][star]  # 卵(5)
        problem += pulp.lpSum(x[5] + x[6] + x[7] + x[15]) <= y[11][star]  # チーズ(4)
        problem += pulp.lpSum(x[4] + x[6] + x[8] + x[16]) <= y[12][star]  # 魚(4)
        problem += pulp.lpSum(x[3] + x[4] + x[8] + x[14] + x[17]) <= y[13][star]  # エビ(5)

        problem.solve(pulp.PULP_CBC_CMD(msg=0))

        pt = pulp.value(problem.objective)
        print("Star {}: {:.0f} pt".format(star+1, pt))
        point_sum += pt

        food_string = ["カレー", "オムライス", "牛丼", "天丼", "寿司", "チーズチキンサンド", "フィッシュバーガー", "チーズホットドッグ", "フィッシュアンドチップス", "ミートソーススパゲティ", "オムそば", "肉うどん", "ラーメン", "ハンバーガー", "海老天うどん", "はしまき", "マグロ丼", "串カツ", "焼きそば", "コロッケ", "和風チキンカツサンド"]
        for i in range(21):
            if int(x[i].value()) > 0:
                print(food_string[i]+"：{:.0f}".format(x[i].value()), end=" ")
        print()

        # 使いきれなかったのは星が一つ小さいものに加える
        if star != 0:
            y[0][star] -= x[0].value() + x[1].value() + x[2].value() + x[3].value() + x[4].value() + x[16].value()
            y[1][star] -= x[5].value() + x[6].value() + x[7].value() + x[13].value() + x[20].value()
            y[2][star] -= x[9].value() + x[10].value() + x[11].value() + x[12].value() + x[14].value() + x[18].value()
            y[3][star] -= x[1].value() + x[5].value() + x[20].value()
            y[4][star] -= x[7].value() + x[12].value() + x[17].value() + x[18].value()
            y[5][star] -= x[2].value() + x[9].value() + x[11].value() + x[13].value()
            y[6][star] -= x[0].value() + x[10].value() + x[11].value() + x[19].value()
            y[7][star] -= x[2].value() + x[3].value() + x[9].value() + x[13].value() + x[17].value() + x[19].value()
            y[8][star] -= x[0].value() + x[8].value() + x[19].value()
            y[9][star] -= x[15].value() + x[16].value() + x[18].value() + x[20].value()
            y[10][star] -= x[1].value() + x[10].value() + x[12].value() + x[14].value() + x[15].value()
            y[11][star] -= x[5].value() + x[6].value() + x[7].value() + x[15].value()
            y[12][star] -= x[4].value() + x[6].value() + x[8].value() + x[16].value()
            y[13][star] -= x[3].value() + x[4].value() + x[8].value() + x[14].value() + x[17].value()
            for i in range(14):
                y[i][star-1] += y[i][star]

    print("Sum：{} pt".format(int(point_sum)))


def parse_argument():
    parser = argparse.ArgumentParser(description="kyujyomeshi solver")
    parser.add_argument("--file_name", "-f", default="sample.csv", help="file name of food data")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    _args = parse_argument()
    df = pd.read_csv(_args.file_name, index_col=0)
    print("食材の個数表")
    print(df)
    print("-----------------")
    print("計算結果")
    solve(df.to_numpy())

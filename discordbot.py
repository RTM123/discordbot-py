import discord
from discord import app_commands

# 봇 초기화
class aclient(discord.Client):
    def __init__(self):
         super().__init__(intents = discord.Intents.all())
         self.synced = False
    async def on_ready(self):
         await self.wait_until_ready()
         if not self.synced: 
             await tree.sync() 
             self.synced = True

client = aclient()
tree = app_commands.CommandTree(client)

# 제작자와 계좌번호 저장
accounts = {
    '로드': '토스뱅크 1908-8928-4262 ㄱㅈㅇ',
    '하린': '토스뱅크 1000-2941-3872 ㅅㅅㄱ',
    '다은': '신한 110-511-977829 ㅅㄷㅇ'
}

@tree.command(name='계산', description='수식을 계산합니다.')
@app_commands.describe(expression='계산할 수식')  # 설명 추가
async def 계산(interaction: discord.Interaction, expression: str):
    try:
        # 입력된 표현식에서 슬래시를 곱셈으로 변경
        expression = expression.replace("/", "*")

        # 공백 제거
        expression = expression.replace(" ", "")

        # 계산
        total_price = eval(expression)  # 변환된 식을 평가

        # 소수점 버리기
        total_price = int(total_price)  # 소수점 제거

        await interaction.response.send_message(f"계산된 가격은 {total_price}원입니다.")
    except ZeroDivisionError:
        await interaction.response.send_message("0으로 나눌 수 없습니다.")
    except ValueError:
        await interaction.response.send_message("잘못된 입력입니다. 예시: `1000/3 + 2000/5` 형식으로 입력해 주세요.")
    except Exception as e:
        await interaction.response.send_message(f"오류가 발생했습니다: {str(e)}")


@tree.command(name='제작자', description='제작자 목록을 보여줍니다.')
async def 제작자(interaction: discord.Interaction):
    embed = discord.Embed(title="제작자 목록", description="원하는 제작자를 선택하세요.", color=0xDDA0DD)
    for name in accounts.keys():
        embed.add_field(name=name, value="", inline=False)

    # Select 메뉴 생성
    class SelectMenu(discord.ui.Select):
        def __init__(self):
            options = [
                discord.SelectOption(label=name, description=f"{name}의 계좌번호 보기") for name in accounts.keys()
            ]
            super().__init__(placeholder="제작자를 선택하세요", options=options)

        async def callback(self, interaction: discord.Interaction):
            selected_creator = self.values[0]
            account_number = accounts[selected_creator]
            # 상호작용한 사람에게만 보이도록 메시지를 전송
            await interaction.response.send_message(f"{selected_creator}의 계좌번호: {account_number}", ephemeral=True)

    # View에 Select 메뉴 추가
    view = discord.ui.View()
    view.add_item(SelectMenu())

    await interaction.response.send_message(embed=embed, view=view)

# 봇 실행
client.run("MTMwMTgzNDY1ODYyNjkzMjc2Ng.GkONbE.YWGGD9enzQ_P4Ymidb8xTEzuqRmqw0J7Lkw6y8")

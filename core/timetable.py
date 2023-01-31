import nextcord
import requests
import io
import plotly.graph_objs as go

class NextcordHandler(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            "Credentials",
            timeout=5 * 60,
        )

        self.userName = nextcord.ui.TextInput(
            label="Username",
            max_length=50,
        )

        self.passWord = nextcord.ui.TextInput(
            label="Password",
            max_length=50,
        )
        self.add_item(self.userName)
        self.add_item(self.passWord)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.defer()
        try:
            response = get_cs_time(self.userName.value, self.passWord.value)
            img_bytes = convert_json_to_png(response.json())
            await interaction.send(file=nextcord.File(img_bytes, filename="timetable.png"))
        except:
            await interaction.send("Something went wrong. Please try again later.")
            return 
        
# function to get cs time
def get_cs_time(username, password):
    url = "https://kuappstore.ku.ac.th/nisitku/nisit/Controller.php"
    # request for token
    login_data = {
        "action": "login",
        "id": username,
        "pass": password,
    }

    response = requests.get(url=url, json=login_data)
    if response.status_code != 200:
        return None
    try:
        # extract token and id 
        token = response.json()[0]["token"]
        id = response.json()[0]["id"]
    except (KeyError, IndexError):
        return None
    # request with token
    cs_time_data = {
        "action": "cs_time",
        "id": id,
        "token": token,
    }
    response = requests.post(url=url, json=cs_time_data)
    return response

# function to convert json to png
def convert_json_to_png(json_data):
    # extract data from json
    days = [i["day"] for i in json_data[0]["cstime"]]
    courses = [i["courses"] for i in json_data[0]["cstime"]]

    #a list to store data
    data = []
    for i, day in enumerate(days):
        for course in courses[i]:
            data.append(
                [
                    day,
                    course["course_name"],
                    course["time"],
                    course["course_id"],
                    course["section"],
                    course["room"],
                ]
            )

    # a table
    fig = go.Figure(data=[go.Table(cells=dict(values=data, align="center"))])

    fig.update_layout(
        title={
            "text": "TimeTable",
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "y": 0.9,
        },
        width=1500,
        height=400,
        font=dict(family="Arial", size=11, color="rgb(0,0,0)"),
        titlefont=dict(family="Arial", size=30, color="rgb(0,0,0)"),
    )

    # binary stream of the img
    img_bytes = io.BytesIO()
    fig.write_image(img_bytes, format='png')
    img_bytes.seek(0)

    return img_bytes




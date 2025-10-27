from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

#TODO Fix recitation hours to be correct for this semester.
RECITATION_HOURS = {"a": "09:00~09:50", "b": "10:00~10:50",
                    "c": "11:00~11:50", "d": "12:00~12:50"}
MICROSERVICE_LINK = "http://17313-teachers2.s3d.cmu.edu:8080/section_info/"


@app.get("/section_info/{section_id}")

def get_section_info(section_id: str):

    if section_id is None:
        raise HTTPException(status_code=404, detail="Missing section id")

    section_id = section_id.lower()

    response = requests.get(MICROSERVICE_LINK + section_id)

    # If the microservice call fails, you should handle that too (e.g., check response.status_code)

    data = response.json()
    ta_name_list = data["ta"]

    # Check if the list has enough elements before accessing indices
    if len(ta_name_list) >= 2:
        ta1_name = ta_name_list[0]
        ta2_name = ta_name_list[1]
    else:
        # Handle cases where there aren't two TAs (e.g., assign defaults or raise an error)
        ta1_name = ta_name_list[0] if len(ta_name_list) >= 1 else "Unknown TA 1"
        ta2_name = "Unknown TA 2"
        
    print(ta1_name, ta2_name)

    # TODO Fix this to return correct values for correct sections.
    if section_id in RECITATION_HOURS:
        [start_time, end_time] = (RECITATION_HOURS[section_id]).split("~")
        return {
            "section": section_id,
            "start_time": start_time,
            "end_time": end_time,
            # ✨ Use the variables you extracted!
            "ta": [ta1_name, ta2_name] 
        }
    else:
        raise HTTPException(status_code=404, detail="Invalid section id")
# def get_section_info(section_id: str):

#     if section_id is None:
#         raise HTTPException(status_code=404, detail="Missing section id")

#     section_id = section_id.lower()

#     response = requests.get(MICROSERVICE_LINK + section_id)

#     # You can check out what the response body looks like in terminal using the print statement
#     data = response.json()
#     print(data)
#     ta_name_list = data["ta"]
#     ta1_name = ta_name_list[0]
#     ta2_name = ta_name_list[1]

#     print(ta1_name)

#     # TODO Fix this to return correct values for correct sections.
#     if section_id in RECITATION_HOURS:
#         [start_time, end_time] = (RECITATION_HOURS[section_id]).split("~")
#         return {
#             "section": section_id,
#             "start_time": start_time,
#             "end_time": end_time,
#             "ta": ["taName1", "taName2"]
#         }
#     else:
#         raise HTTPException(status_code=404, detail="Invalid section id")

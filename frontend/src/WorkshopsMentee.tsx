import React, { useEffect } from "react";
import "./App.css";
import axios from "axios";
import NavBarMentee from "./components/NavBarMentee";
import { BiMap, BiWrench } from "react-icons/bi";

interface UserData {
  id?: number;
  firstName: string;
  lastName: string;
  avatar: string;
  role: string;
  businessArea: string;
  topics?: string[];
}

interface Workshop {
  workshopID: number;
  mentorID: number;
  title: string;
  description: string;
  topic: string;
  location: string;
  status: string; // going-ahead, cancelled, running, completed
  startTime: Date;
  endTime: Date;
}

interface CardProps {
  workshopData: Workshop;
}

function parseDateStr(d: string) {
  const [date, time] = d.split(" ");
  const [day, month, year] = date.split("/");
  const [hour, min] = time.split(":");
  const fullYear = "20" + year;

  return new Date(
    new Date(
      parseInt(fullYear),
      parseInt(month) - 1,
      parseInt(day),
      parseInt(hour),
      parseInt(min)
    )
  );
}

function parseDate(d: Date) {
  const month = d.toLocaleString("default", { month: "long" });
  const date =
    month +
    " " +
    d.getDate() +
    ", " +
    d.getFullYear() +
    ", " +
    d.getHours() +
    ":" +
    d.getMinutes();

  return date;
}

const WorkshopCard: React.FC<CardProps> = (props) => {
  const workshop = props.workshopData;

  const start: string = parseDate(workshop.startTime);
  const end: string = parseDate(workshop.endTime);

  let labelText: string = workshop.status;
  if (labelText === "going-ahead") labelText = "upcoming";

  let labelColour: string = "";
  switch (labelText) {
    case "upcoming":
      labelColour = "bg-brightNavyBlue";
      break;
    case "completed":
      labelColour = "bg-prussianBlue";
      break;
    case "cancelled":
      labelColour = "bg-firebrick";
      break;
  }

  return (
    <div className="flex flex-col bg-gray-300 bg-opacity-50 shadow-md m-auto mt-5 mb-5 w-[70%] text-prussianBlue p-8 pr-5 pl-5 rounded-xl text-left">
      {/* Workshop title and status */}
      <div className="flex flex-col mb-3 w-[100%] border-b-2 pb-5 border-imperialRed">
        {/* Title and label */}
        <div className="flex flex-row justify-between mr-4 ml-4">
          <div className="flex flex-row mt-1 mb-6 text-firebrick">
            <BiWrench className="m-auto text-5xl mr-3" />
            <h1 className="text-3xl font-semibold text-left m-auto">
              {workshop.title}
            </h1>
          </div>

          <p
            className={
              "text-cultured rounded-full font-body text-sm m-auto mr-0 mt-0 p-1 pl-3 pr-3 " +
              labelColour
            }
          >
            {labelText.toUpperCase()}
          </p>
        </div>

        <div className="flex flex-row justify-between mr-4 ml-4">
          <div className="flex flex-col space-y-2">
            <h2 className="text-2xl font-semibold">{workshop.topic}</h2>
            <div className="flex flex-row">
              <BiMap className="text-2xl m-auto ml-0 mr-1" />
              <h3 className="text-lg">{workshop.location}</h3>
            </div>
          </div>

          {/* Start and end times */}
          <div className="flex flex-row flex-none text-right">
            <h1 className="text-lg m-auto overflow-auto text-clip">
              <span className="font-semibold">Start: </span>
              {start}
              <br></br>
              <span className="font-semibold">End: </span>
              {end}
            </h1>
            {/* <BiCalendar className="text-5xl m-auto mr-2 ml-2" /> */}
          </div>
        </div>
      </div>

      <div className="text-justify text-lg mr-4 ml-4 mt-3">
        <span className="font-bold">Description:</span> {workshop.description}
      </div>
    </div>
  );
};

function WorkshopsMentee() {
  const [user, setUser] = React.useState<UserData>({
    firstName: "",
    lastName: "",
    avatar: "",
    role: "",
    businessArea: "",
    topics: [],
  });
  const [workshops, setWorkshops] = React.useState<Workshop[]>([]);

  // Get user data
  useEffect(() => {
    axios.get("/api/users/get-own-data").then(async (res) => {
      const newUser: UserData = {
        id: res.data.userid,
        firstName: res.data.firstname,
        lastName: res.data.lastname,
        avatar: res.data.profilepicture,
        role: res.data.role,
        businessArea: res.data.businessarea,
      };

      setUser(newUser);
    });
  }, []);

  // Get workshops associated with user
  useEffect(() => {
    if (user.id !== -1 && user.role !== "")
      axios
        .get("/api/workshop/get-workshops", {
          params: { userID: user.id, role: user.role },
        })
        .then(async (res: any) => {
          console.log(res.data);

          var newRunningWorkshops: Workshop[] = [];
          var newGoingAheadWorkshops: Workshop[] = [];
          var newCompletedWorkshops: Workshop[] = [];
          var newCancelledWorkshops: Workshop[] = [];

          // // New - requests attendees - doesn't work
          // var newWorkshops: Workshop[] = [];
          // for (const workshop of res.data) {
          //   let attendees = [];

          //   await axios
          //     .get("/api/workshop/view-workshop-attendee", {
          //       params: { workshopID: workshop.workshopid },
          //     })
          //     .then((res) => {
          //       console.log(res.data);
          //       attendees = res.data.map((a: any) => {
          //         return {
          //           goalID: a.planofactionid,
          //           title: a.title,
          //           description: a.description,
          //           status: a.status,
          //         };
          //       });

          //       newWorkshops.push({
          //         workshopID: workshop.workshopid,
          //         mentorID: workshop.mentorid,
          //         title: workshop.title,
          //         description: workshop.description,
          //         topic: workshop.topic,
          //         location: workshop.location,
          //         status: workshop.status,
          //         startTime: parseDateStr(workshop.starttime),
          //         endTime: parseDateStr(workshop.endtime),
          //       })
          //     });
          // }

          // works but old version that doesn't show attendees
          const newWorkshops: Workshop[] = res.data.map((w: any) => {
            return {
              workshopID: w.workshopid,
              mentorID: w.mentorid,
              title: w.title,
              description: w.description,
              topic: w.topic,
              location: w.location,
              status: w.status,
              startTime: parseDateStr(w.starttime),
              endTime: parseDateStr(w.endtime),
            };
          });

          for (const w of newWorkshops) {
            switch (w.status) {
              case "running":
                newRunningWorkshops.push(w);
                break;
              case "going-ahead":
                newGoingAheadWorkshops.push(w);
                break;
              case "completed":
                newCompletedWorkshops.push(w);
                break;
              case "cancelled":
                newCancelledWorkshops.push(w);
                break;
              default:
                break;
            }
          }

          // Sorting meetings - from closest to most distant
          newRunningWorkshops.sort((e1: any, e2: any) => {
            return e1.startTime - e2.startTime;
          });
          newGoingAheadWorkshops.sort((e1: any, e2: any) => {
            return e1.startTime - e2.startTime;
          });

          newCompletedWorkshops.sort((e1: any, e2: any) => {
            return e2.startTime - e1.startTime;
          });
          newCancelledWorkshops.sort((e1: any, e2: any) => {
            return e2.startTime - e1.startTime;
          });

          // console.log(newWorkshops);
          setWorkshops([
            ...newRunningWorkshops,
            ...newGoingAheadWorkshops,
            ...newCompletedWorkshops,
            ...newCancelledWorkshops,
          ]);
        });
  }, [user]);

  return (
    <div className="fixed h-full w-full">
      <NavBarMentee activeStr="Workshops" />

      {/* Main flexbox */}
      <div className="h-full w-full font-display bg-cultured overflow-auto p-6 flex flex-col pb-40">
        {workshops.map((workshop) => {
          return <WorkshopCard workshopData={workshop} />;
        })}
      </div>
    </div>
  );
}

export default WorkshopsMentee;

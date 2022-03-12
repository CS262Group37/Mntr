import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  BiUserCircle,
  BiEnvelope,
  BiBell,
  BiCog,
  BiLogOut,
  BiCalendar,
} from "react-icons/bi";
import { Link } from "react-router-dom";
import Event from "./Event";

interface UserData {
  id?: number;
  firstName: string;
  lastName: string;
  avatar: string;
  role: string;
}

interface Meeting {
  meetingID: number;
  title: string;
  feedback: string;
  status: string; // going-ahead, cancelled, running, completed, missed, pending
  startTime: Date;
  mentor: UserData; // is called mentor but can be either mentee or mentor (for consistency with workshop property)
}

interface Workshop {
  workshopID: number;
  title: string;
  topic: string;
  location: string;
  status: string; // going-ahead, cancelled, running, completed
  startTime: Date;
  mentor: UserData;
}

interface UserMenuProps {
  user: UserData;
}

interface MessageProps {
  subject: string;
  content: string;
  sender: string;
  senderID: number;
  // date: Date;
}

interface NotifProps {
  contents: string;
}

// const Event: React.FC<EventProps> = (props) => {
//   return (
//     <div className="font-body text-base bg-gray-300 rounded-md p-3 mt-3 ml-2 bg-opacity-50 shadow-sm">
//       <div className="flex flex-row justify-between">
//         <p className="font-semibold text-firebrick">{props.title}</p>
//         <p
//           className={
//             "text-cultured rounded-full text-sm m-auto mr-1 p-1 pl-3 pr-3 " +
//             (props.type === "Workshop" ? "bg-imperialRed" : "bg-brightNavyBlue")
//           }
//         >
//           {props.type}
//         </p>
//       </div>

//       <p className="font-bold">
//         {props.date.toLocaleDateString() +
//           " at " +
//           props.date.toLocaleTimeString()}
//       </p>

//       <p>
//         <span className="font-semibold">Mentors: </span>
//         {props.mentors.map((mentor, i, { length }) => {
//           if (i === length - 1) {
//             return <span>{mentor}</span>;
//           } else return <span>{mentor + ", "}</span>;
//         })}
//       </p>
//     </div>
//   );
// };

const logout = async () => {
  try {
    axios.get("/api/auth/logout");
  } catch (error: any) {
    console.log(error.response);
  }
};

const Message: React.FC<MessageProps> = (props) => {
  return (
    <div className="font-body text-base bg-gray-300 rounded-md p-3 mt-3 ml-2 bg-opacity-50 shadow-sm">
      <p className="font-semibold text-firebrick">
        <span className="font-normal">From: </span>
        <Link to={"/profile?id=" + props.senderID} className="hover:underline">{props.sender}</Link>
      </p>
      <p className="font-semibold">{props.subject}</p>
      <p>{props.content}</p>
    </div>
  );
};

const Notification: React.FC<NotifProps> = (props) => {
  return (
    <div className="font-body text-base bg-gray-300 rounded-md p-3 mt-3 ml-2 bg-opacity-50 shadow-sm">
      <p>{props.contents}</p>
    </div>
  );
};

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

const UserMenu: React.FC<UserMenuProps> = (props) => {
  const [messages, setMessages] = useState<MessageProps[]>([]);
  const [meetings, setMeetings] = useState<Meeting[]>([]);
  const [workshops, setWorkshops] = useState<Workshop[]>([]);

  const getMessages = () => {
    axios.get("api/messages/get-emails").then(async (res) => {
      console.log(res.data);
      const newMessages: MessageProps[] = [];
      for (const msg of res.data) {
        await axios
          .post("api/users/get-user-data", { userID: msg.senderid })
          .then((res) => {
            const newMsg = {
              sender: `${res.data.firstname} ${res.data.lastname}`,
              senderID: res.data.userid,
              subject: msg.subject,
              content: msg.content,
            };
            newMessages.push(newMsg);
          });
      }
      setMessages(newMessages);
    });
  };

  useEffect(() => {
    getMessages();
  }, []);

  const getMeetings = () => {
    axios.get("/api/relations/get-relations").then(async (res: any) => {
      var newRunningMeetings: Meeting[] = [];
      var newGoingAheadMeetings: Meeting[] = [];

      for (const relationship of res.data) {
        // Get user data
        let menteeMentor: UserData;
        const userID = (props.user.role === "mentor" ? relationship.menteeid : relationship.mentorid);

        await axios
          .post("/api/users/get-user-data", { userID: userID })
          .then((res: any) => {
            menteeMentor = {
              id: userID,
              firstName: res.data.firstname,
              lastName: res.data.lastname,
              avatar: res.data.profilepicture,
              role: res.data.role,
            };
          });

        // Get meetings
        let newMeetings: Meeting[];
        await axios
          .post("/api/meetings/get-meetings", {
            relationID: relationship.relationid,
          })
          .then((res: any) => {
            newMeetings = res.data.map((m: any) => {
              return {
                meetingID: m.meetingid,
                title: m.title,
                description: m.description,
                feedback: m.feedback,
                status: m.status,
                startTime: parseDateStr(m.starttime),
                endTime: parseDateStr(m.starttime),
                mentor: menteeMentor,
              };
            });

            newMeetings.sort((e1: any, e2: any) => {
              return e2.startTime - e1.startTime;
            });

            for (const meeting of newMeetings) {
              switch (meeting.status) {
                case "running":
                  newRunningMeetings.push(meeting);
                  break;
                case "going-ahead":
                  newGoingAheadMeetings.push(meeting);
                  break;
                default:
                  break;
              }
            }

            // Sorting meetings - from closest to most distant
            newRunningMeetings.sort((e1: any, e2: any) => {
              return e1.startTime - e2.startTime;
            });
            newGoingAheadMeetings.sort((e1: any, e2: any) => {
              return e1.startTime - e2.startTime;
            });
          });
      }

      setMeetings([ ...newRunningMeetings, ...newGoingAheadMeetings]);
    });
  };

  const getWorkshops = () => {
    axios
      .get("/api/workshop/get-workshops", {
        params: { userID: props.user.id, role: props.user.role },
      })
      .then(async (res: any) => {
        var newRunningWorkshops: Workshop[] = [];
        var newGoingAheadWorkshops: Workshop[] = [];

        for (const workshop of res.data) {
          let mentor: UserData = {firstName: "", lastName: "", avatar: "", role: ""};

          await axios
          .post("/api/users/get-user-data", { userID: workshop.mentorid })
          .then((res: any) => {
            mentor = {
              id: workshop.mentorid,
              firstName: res.data.firstname,
              lastName: res.data.lastname,
              avatar: res.data.profilepicture,
              role: res.data.role,
            };
          });

          const newWorkshop = {
            workshopID: workshop.workshopid,
            title: workshop.title,
            topic: workshop.topic,
            location: workshop.location,
            status: workshop.status,
            startTime: parseDateStr(workshop.starttime),
            mentor: mentor,
          }

          switch (newWorkshop.status) {
            case "running":
              newRunningWorkshops.push(newWorkshop);
              break;
            case "going-ahead":
              newGoingAheadWorkshops.push(newWorkshop);
              break;
            default:
              break;
          };
        }

        // Sorting meetings - from closest to most distant
        newRunningWorkshops.sort((e1: any, e2: any) => {
          return e1.startTime - e2.startTime;
        });
        newGoingAheadWorkshops.sort((e1: any, e2: any) => {
          return e1.startTime - e2.startTime;
        });

        setWorkshops([ ...newRunningWorkshops, ...newGoingAheadWorkshops]);
      });
  };

  useEffect(() => {
    getMeetings();
    getWorkshops();    
  }, []);

  useEffect(() => {
    console.log(meetings);
    console.log(workshops);
  }, []);

  return (
    <div
      className={
        "bg-cultured rounded-xl text-prussianBlue flex-auto w-[500px] max-h-[640px] overflow-auto top-20 right-6 z-10 pt-2 text-left animate-growDown origin-top-right text-xl font-display"
      }
    >
      <Link
        to={"/profile?id=" + props.user.id}
        className="flex flex-row font-semibold text-2xl hover:font-bold pr-6 pl-6 pb-4 pt-4 border-b-[1px] border-gray-300"
      >
        <BiUserCircle className="text-3xl m-auto ml-0 mr-2" />
        <h2>{props.user.firstName + " " + props.user.lastName}</h2>
      </Link>

      {/* Notifications */}
      <div className="pr-6 pl-6 pb-4 pt-4 border-b-[1px] border-gray-300">
        <div className="flex flex-row">
          <BiBell className="text-2xl m-auto ml-0 mr-2" />
          <h2>Notifications</h2>
        </div>

        <div className="flex flex-col mt-1">
          <Notification contents="Notification 1" />
          <Notification contents="Notification 2" />
          <Notification contents="Notification 3" />
        </div>
      </div>

      {/* Messages */}
      <div className="pr-6 pl-6 pb-4 pt-4 border-b-[1px] border-gray-300">
        <div className="flex flex-row">
          <BiEnvelope className="text-2xl m-auto ml-0 mr-2" />
          <h2>My messages</h2>
        </div>

        <div className="flex flex-col mt-1">
          {messages.map((msg) => {
            return (
              <Message
                sender={msg.sender}
                subject={msg.subject}
                content={msg.content}
                senderID={msg.senderID}
              />
            );
          })}
        </div>
      </div>

      {/* Events */}
      <div className="pr-6 pl-6 pb-4 pt-4">
        <div className="flex flex-row">
          <BiCalendar className="text-2xl m-auto ml-0 mr-2" />
          <h2>Upcoming events</h2>
        </div>

        {/* sample events */}
        <div className="flex flex-col mt-1">
          {/* <Event
            date={new Date("2022-02-25")}
            title="Sample event 1"
            type="Individual"
            mentors={["John Doe"]}
          />
          <Event
            date={new Date("2022-02-27")}
            title="Sample event 2"
            type="Workshop"
            mentors={["John Doe", "Jane Doe"]}
          /> */}
          {
          meetings.map((m) => {
            return <Event event={m} />
          })
        }
        {
          workshops.map((w) => {
            return <Event event={w} />
          })
        }
        </div>
      </div>

      <div className="flex flex-row justify-between bottom-0 sticky bg-inherit pb-2 border-t-[1px] border-gray-300">
        <Link
          to="/settings"
          className="flex flex-row hover:font-semibold pr-6 pl-6 pb-4 pt-4"
        >
          <BiCog className="text-2xl m-auto ml-0 mr-2" />
          <h2>Settings</h2>
        </Link>

        <Link
          to="/"
          className="flex flex-row hover:font-semibold pr-6 pl-6 pb-4 pt-4"
        >
          <span onClick={logout}>Log out</span>
          <BiLogOut className="text-2xl m-auto mr-0 ml-2" />
        </Link>
      </div>
    </div>
  );
};

export default UserMenu;

import { Avatar, Divider } from "@mui/material";
import React from "react";
import { BiCalendarEvent, BiMap, BiChat } from "react-icons/bi";
import { Link } from "react-router-dom";

interface EventProps {
  event: Meeting | Workshop;
}

interface Meeting {
  meetingID: number;
  title: string;
  status: string; // going-ahead, cancelled, running, completed, missed, pending
  startTime: Date;
  mentor: UserData;
  location?: any;
  topic?: any;
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

interface UserData {
  id?: number;
  firstName: string;
  lastName: string;
  avatar: string;
  role: string;
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

const Event: React.FC<EventProps> = (props) => {
  const event: Workshop | Meeting = props.event;
  const type: string = (event.hasOwnProperty("meetingID") ? "Meeting" : "Workshop"); // determine whether event is workshop or meeting

  return (
    <div className="font-body text-base bg-gray-300 rounded-md p-2 mt-3 ml-2 bg-opacity-50 shadow-sm flex flex-col space-y-[5px]">
      <div className="flex flex-row justify-between mb-1 p-2 pb-1">
        <p className="font-semibold text-firebrick pr-5">{event.title}</p>
        <p
          className={
            "text-cultured rounded-full text-sm m-auto mr-1 mt-0 p-1 pl-3 pr-3 select-none " +
            (type === "Workshop" ? "bg-imperialRed" : "bg-brightNavyBlue")
          }
        >
          {type.toUpperCase()}
        </p>
      </div>

      <Divider />

      {/* Date */}
      <div className="flex flex-row p-2 pt-1 pb-1">
        <BiCalendarEvent className="m-auto ml-0 mr-1 text-xl" />
        <p className="">
          {parseDate(event.startTime)}
        </p>
      </div>

      {type === "Meeting" &&
      <>
      <Divider />
      <div className="flex flex-row p-2">
        <Avatar
          alt={event.mentor.firstName + " " + event.mentor.lastName}
          src={event.mentor.avatar}
          sx={{ width: 28, height: 28 }}
        />
        <Link to={"/profile?id=" + event.mentor.id} className="hover:font-semibold m-auto ml-2">{event.mentor.firstName + " " + event.mentor.lastName}</Link>
      </div>
      </>
      }

      {/* Display topic and location for workshops */}
      {type === "Workshop" && 
      <>
      <div className="flex flex-row p-2 pt-1 pb-1">
        <BiChat className="m-auto ml-0 mr-1 text-xl min-w-[20px]"/>
        <p className="">
          {event.topic}
        </p>
      </div>
      <div className="flex flex-row p-2 pt-1 pb-1">
        <BiMap className="m-auto ml-0 mr-1 text-xl min-w-[20px]"/>
        <p className="">
          {event.location}
        </p>
      </div>
      </>
      }

      {/* Display mentor name for workshops */}
      {type === "Workshop" && 
      <p className="p-2 pt-1 pb-1">
        <span className="font-semibold">Led by: </span>
        <Link to={"/profile?id=" + event.mentor.id} className="hover:font-semibold">
          {event.mentor.firstName + " " + event.mentor.lastName}
        </Link>
        {/* {props.mentors.map((mentor, i, { length }) => {
          if (i === length - 1) {
            return <span>{mentor}</span>;
          } else return <span>{mentor + ", "}</span>;
        })} */}
      </p>}
    </div>
  );
};

export default Event;

// Meeting component
import { Avatar, Divider, Tooltip } from "@mui/material";
import axios from "axios";
import React from "react";
import {
  BiCalendarCheck,
  BiX,
  BiCheck,
  BiCalendarExclamation,
  BiCalendarEvent,
  BiCalendarX,
  BiCalendar,
  BiCalendarStar,
} from "react-icons/bi";
import { Link } from "react-router-dom";

interface Meeting {
  meetingID: number;
  title: string;
  description: string;
  feedback: string;
  status: string;
  startTime: Date;
  endTime: Date;
  user: UserData;
}

interface UserData {
  id?: number;
  firstName: string;
  lastName: string;
  avatar: string;
  role: string;
}

interface MeetingProps {
  meetingData: Meeting;
  handleNewMeeting: () => void;
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

const MeetingElement: React.FC<MeetingProps> = (props) => {
  const meeting: Meeting = props.meetingData;

  const acceptMeeting = () => {
    axios
      .put("/api/meetings/accept-meeting", { meetingID: meeting.meetingID })
      .then((res) => {
        console.log(res.status);
        props.handleNewMeeting();
      });
  };

  const cancelMeeting = () => {
    axios
      .put("/api/meetings/cancel-meeting", { meetingID: meeting.meetingID })
      .then((res) => {
        console.log(res.status);
        props.handleNewMeeting();
      });
  };

  const date: string = parseDate(meeting.startTime);

  let labelText: string = meeting.status;
  if (labelText === "going-ahead") labelText = "upcoming";

  let labelColour: string = "";

  switch (labelText) {
    case "running":
      labelColour = "bg-yellow-500";
      break;
    case "pending":
      labelColour = "bg-brightNavyBlue";
      break;
    case "completed":
      labelColour = "bg-prussianBlue";
      break;
    case "missed":
      labelColour = "bg-imperialRed";
      break;
    case "cancelled":
      labelColour = "bg-firebrick";
      break;
    case "upcoming":
      labelColour = "bg-green-500";
      break;
  }

  return (
    <div className="flex flex-col bg-gray-300 bg-opacity-50 shadow-md m-5 mr-6 ml-6 text-prussianBlue p-4 pt-1 rounded-xl">
      {meeting.status === "pending" && (
        <div>
          <div className="flex flex-col mt-3 mb-2 text-center">
            <h1 className="text-2xl font-semibold">Accept meeting?</h1>

            <div className="flex flex-row justify-center pr-[44%] pl-[44%]">
              <Tooltip title="Accept" arrow>
                <button
                  className="bg-transparent border-2 border-green-500 text-green-500 text-xl p-1  rounded-full transition ease-in-out hover:bg-green-500 hover:text-cultured duration-200 m-3"
                  onClick={acceptMeeting}
                >
                  <BiCheck className="h-10 w-10 p-1" />
                </button>
              </Tooltip>

              <Tooltip title="Decline" arrow>
                <button
                  className="bg-transparent border-2 border-imperialRed text-imperialRed text-xl p-1 rounded-full transition ease-in-out hover:bg-imperialRed hover:text-cultured duration-200 m-3"
                  onClick={cancelMeeting}
                >
                  <BiX className="h-10 w-10 p-1" />
                </button>
              </Tooltip>
            </div>
          </div>
          <Divider />
        </div>
      )}

      {/* Heading & date */}
      <div className="flex flex-row text-2xl justify-between border-b-2 border-imperialRed mt-3">
        {/* Meeting title and date */}
        <div className="flex flex-col ml-3 mb-3 w-[100%]">
          {/* Title and label */}
          <div className="flex flex-row justify-between">
            <h1 className="font-semibold mt-1 mb-3 text-left">
              {meeting.title}
            </h1>

            <p
              className={
                "text-cultured rounded-full font-body text-sm m-auto mr-2 p-1 pl-3 pr-3 " +
                labelColour
              }
            >
              {labelText.toUpperCase()}
            </p>
          </div>

          <div className="flex flex-row flex-none text-left">
            {meeting.status === "completed" && (
              <BiCalendarCheck className="text-2xl m-auto ml-0 mr-1" />
            )}
            {meeting.status === "going-ahead" && (
              <BiCalendar className="text-2xl m-auto ml-0 mr-1" />
            )}
            {meeting.status === "missed" && (
              <BiCalendarExclamation className="text-2xl m-auto ml-0 mr-1" />
            )}
            {meeting.status === "pending" && (
              <BiCalendarEvent className="text-2xl m-auto ml-0 mr-1" />
            )}
            {meeting.status === "cancelled" && (
              <BiCalendarX className="text-2xl m-auto ml-0 mr-1" />
            )}
            {meeting.status === "running" && (
              <BiCalendarStar className="text-2xl m-auto ml-0 mr-1" />
            )}
            <h1 className="text-lg">{date}</h1>
          </div>
        </div>
      </div>

      <div className="text-justify text-lg p-3 pb-1">
        <span className="font-bold">Description:</span> {meeting.description}
      </div>

      {/* Mentor feedback */}
      {meeting.status === "completed" && (
        // <div className="font-body text-md text-justify p-3 pb-1 border-t-2 border-imperialRed">
        //   <p>{meeting.feedback}</p>
        // </div>
        <div className="bg-cultured rounded-lg p-4 pb-2 font-body m-4">
          <div className="flex flex-row text-2xl justify-between">
            <h1 className="font-bold mt-2 mb-0 ml-3 mr-2 text-left font-display text-lg">
              FEEDBACK
            </h1>
          </div>

          <div className="m-3 text-justify space-y-1">
            <p>{meeting.feedback}</p>
          </div>
        </div>
      )}

      <Divider sx={{ marginTop: 1.5, marginBottom: 1 }} />

      {/* Mentee name + profile pic */}
      <Link to={"/profile?id=" + meeting.user.id} className="flex flex-row p-3 pb-2 hover:font-semibold cursor-pointer group">
        <Avatar
          className="border-2 border-imperialRed"
          alt={meeting.user.firstName + " " + meeting.user.lastName}
          src={meeting.user.avatar}
          sx={{ width: 46, height: 46 }}
        />
        <h2 className="text-2xl m-auto ml-3 peer">
          {meeting.user.firstName + " " + meeting.user.lastName}
        </h2>
      </Link>
    </div>
  );
};

export default MeetingElement;

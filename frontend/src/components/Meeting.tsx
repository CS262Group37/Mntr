import React from "react";
import { BiCalendarCheck } from "react-icons/bi";

// TODO divide feedback into paragraphs?

interface MeetingObject {
  date: Date,
  feedback: string
}

function Meeting(props: MeetingObject) {
  const month = props.date.toLocaleString("default", {month: "long"});
  const date = month + " " + props.date.getDate() + ", " + props.date.getFullYear();

  return(
    <div className="flex flex-col bg-gray-300 bg-opacity-50 shadow-md mt-5 mb-5 w-[100%] text-prussianBlue p-4 rounded-xl">

      {/* Heading & date */}
      <div className="flex flex-row text-2xl border-b-2 border-imperialRed justify-between">
        <h1 className="font-semibold mt-1 mb-3 ml-3">Individual meeting</h1>
        <div className="flex flex-row mr-3 mt-1 mb-3">
          <BiCalendarCheck className="text-3xl mr-1" />
          <h1>{date}</h1>
        </div>
      </div>

      {/* Mentor feedback */}
      <div className="font-body text-lg text-justify m-3 mb-1">
        <p>{props.feedback}</p>
      </div>
    </div>
  );
}

export default Meeting;
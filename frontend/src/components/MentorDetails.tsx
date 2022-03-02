import React from "react";
import { BiUserCircle, BiCalendarEvent } from "react-icons/bi";

interface MentorObject {
  firstName: string;
  lastName: string;
  topic: string;
  nextMeeting: Date;
}

function MentorDetails(props: MentorObject) {
  // TODO schedule a meeting function
  const schedule = () => {
    return;
  };

  // Next meeting date formatting
  const weekday = props.nextMeeting.toLocaleString("default", {weekday: "long"});
  const month = props.nextMeeting.getMonth() + 1;
  const date = weekday + ", " + props.nextMeeting.getDate() + "." + month + "." + props.nextMeeting.getFullYear();

  return (
    <div className="flex flex-col m-10 mb-2 text-firebrick font-display">
      <div className="flex flex-row h-min">
        <div className="flex">
          {/* TODO Mentor profile pic */}
          <BiUserCircle className="text-8xl" />

          {/* Mentor name & topic */}
          <div className="flex flex-col text-left m-auto pl-4 space-y-1">
            <h2 className="font-semibold text-3xl">
              {props.firstName + " " + props.lastName}
            </h2>
            <h3 className="text-xl">{props.topic}</h3>
          </div>
        </div>

        {/* Schedule meeting button */}
        <button
          className="bg-prussianBlue text-cultured text-xl w-64 p-4 m-auto rounded-full shadow-md transition ease-in-out hover:bg-brightNavyBlue duration-200 mr-2"
          onClick={schedule}
        >
          Schedule a meeting
        </button>
      </div>

      {/* Next meeting date */}
      <div className="flex flex-row text-lg font-body m-5">
        <BiCalendarEvent className="mt-auto mb-auto text-3xl mr-1" />
        <p className="mt-auto mb-auto">
          Your next meeting with {props.firstName} is on{" "}
          <span className="font-bold">{date}</span>
        </p>
      </div>
    </div>
  );
}

export default MentorDetails;

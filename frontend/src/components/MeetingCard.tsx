// Meeting component
import React from "react";
import { BiCalendarCheck } from "react-icons/bi";

interface Meeting {
  meetingID: number;
  title: string;
  description: string;
  feedback: string;
  status: string;
  startTime: Date;
  endTime: Date;
}

interface MeetingProps {
  meetingData: Meeting;
}

const MeetingCard: React.FC<MeetingProps> = (props) => {
  const meeting: Meeting = props.meetingData;

  const month = meeting.startTime.toLocaleString("default", { month: "long" });
  const date =
    month + " " + meeting.startTime.getDate() + ", " + meeting.startTime.getFullYear();

  const dummyText1 =
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In ornare in ut iaculis sapien, id orci, pulvinar dui. Dui pulvinar eget varius et, et elit vitae, blandit. Nam in risus laoreet tellus. Pellentesque id ultrices rhoncus viverra nullam pretium tristique quam. Nibh felis posuere in non lectus est. Quis nullam porta sed pellentesque dui. Sed phasellus in vitae mi amet enim blandit. Eu neque viverra aenean porta cras. Aliquam rhoncus, faucibus imperdiet elementum. Ac praesent condimentum massa nam eu. Duis tellus aenean nunc id interdum. Mattis imperdiet fringilla purus tortor, egestas interdum. Eget posuere vel semper maecenas aliquet vulputate mattis aliquet.";

  if (meeting.feedback === null)
    meeting.feedback = dummyText1;

  return (
    <div className="flex flex-col bg-gray-300 bg-opacity-50 shadow-md mt-5 mb-5 w-[100%] text-prussianBlue p-4 rounded-xl">
      {/* Heading & date */}
      <div className="flex flex-row text-2xl border-b-2 border-imperialRed justify-between">
        <h1 className="font-semibold mt-1 mb-3 ml-3 text-left">
          Individual meeting
        </h1>
        <div className="flex flex-row mr-3 mt-1 mb-3 text-right">
          <BiCalendarCheck className="text-3xl mr-1" />
          <h1>{date}</h1>
        </div>
      </div>

      {/* Mentor feedback */}
      <div className="font-body text-md text-justify m-3 mb-1">
        <p>{meeting.feedback}</p>
      </div>
    </div>
  );
};

export default MeetingCard;
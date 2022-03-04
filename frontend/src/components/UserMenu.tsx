import React from "react";
import {
  BiUserCircle,
  BiEnvelope,
  BiBell,
  BiCog,
  BiLogOut,
  BiCalendar,
} from "react-icons/bi";
import { Link } from "react-router-dom";

interface UserMenuProps {
  visible: boolean;
}

interface EventProps {
  date: Date;
  title: string;
  type: string; // "Workshop" or "Individual"
  mentors: string[];
  attendees?: any;
}

interface MessageProps {
  contents: string;
  sender: string;
  // date: Date;
}

interface NotifProps {
  contents: string;
}

const Event: React.FC<EventProps> = (props) => {
  return (
    <div className="font-body text-base bg-gray-300 rounded-md p-3 mt-3 ml-2 bg-opacity-50 shadow-sm">
      <div className="flex flex-row justify-between">
        <p className="font-semibold text-firebrick">{props.title}</p>
        <p
          className={
            "text-cultured rounded-full text-sm m-auto mr-1 p-1 pl-3 pr-3 " +
            (props.type === "Workshop" ? "bg-imperialRed" : "bg-brightNavyBlue")
          }
        >
          {props.type}
        </p>
      </div>

      <p className="font-bold">
        {props.date.toLocaleDateString() +
          " at " +
          props.date.toLocaleTimeString()}
      </p>

      <p>
        <span className="font-semibold">Mentors: </span>
        {props.mentors.map((mentor, i, { length }) => {
          if (i === length - 1) {
            return <span>{mentor}</span>;
          } else return <span>{mentor + ", "}</span>;
        })}
      </p>
    </div>
  );
};

const Message: React.FC<MessageProps> = (props) => {
  return (
    <div className="font-body text-base bg-gray-300 rounded-md p-3 mt-3 ml-2 bg-opacity-50 shadow-sm">
      <p className="font-semibold text-firebrick">
        <span className="font-normal">From: </span>
        {props.sender}
      </p>
      <p>{props.contents}</p>
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

const UserMenu: React.FC<UserMenuProps> = (props) => {
  return (
    <div
      className={
        "absolute bg-cultured text-prussianBlue w-1/3 flex-auto max-h-[66%] overflow-auto top-20 right-6 z-10 pt-2 text-left rounded-3xl shadow-md animate-growDown origin-top-right inline-block text-xl font-display " +
        (props.visible ? "visible" : "hidden")
      }
    >
      <Link
        to="/dashboard-mentee"
        className="flex flex-row hover:font-semibold pr-6 pl-6 pb-4 pt-4 border-b-[1px] border-gray-300"
      >
        <BiUserCircle className="text-2xl m-auto ml-0 mr-2" />
        <h2>View public profile</h2>
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
          <Message sender="Bruh Bruh" contents="Sample message" />
          <Message sender="Bruh Moment" contents="Sample message 2" />
          <Message sender="Bruh Bruh" contents="Sample message 3" />
        </div>
      </div>

      {/* Events */}
      <div className="pr-6 pl-6 pb-4 pt-4 border-b-[1px] border-gray-300">
        <div className="flex flex-row">
          <BiCalendar className="text-2xl m-auto ml-0 mr-2" />
          <h2>Upcoming events</h2>
        </div>

        {/* sample events */}
        <div className="flex flex-col mt-1">
          <Event
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
          />
        </div>
      </div>

      <div className="flex flex-row justify-between bottom-0 sticky bg-inherit pb-2 border-t-[1px] border-gray-300">
        <Link
          to="/dashboard-mentee"
          className="flex flex-row hover:font-semibold pr-6 pl-6 pb-4 pt-4"
        >
          <BiCog className="text-2xl m-auto ml-0 mr-2" />
          <h2>Settings</h2>
        </Link>

        <Link
          to="/"
          className="flex flex-row hover:font-semibold pr-6 pl-6 pb-4 pt-4"
        >
          <h2>Log out</h2>
          <BiLogOut className="text-2xl m-auto mr-0 ml-2" />
        </Link>
      </div>
    </div>
  );
};

export default UserMenu;

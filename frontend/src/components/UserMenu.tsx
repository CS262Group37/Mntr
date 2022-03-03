import React from "react";
import {
  BiUserCircle,
  BiEnvelope,
  BiBell,
  BiCog,
  BiLogOut,
} from "react-icons/bi";
import { Link } from "react-router-dom";

interface UserMenuProps {
  visible: boolean;
}

interface MessageProps {
  contents: string;
  sender: string;
  // date: Date;
}

interface NotifProps {
  contents: string;
}

const Message: React.FC<MessageProps> = (props) => {
  return (
    <div className="font-body text-base bg-gray-300 rounded-md p-3 mt-3 ml-2 bg-opacity-50 shadow-sm">
      <p className="font-semibold text-firebrick">{props.sender}</p>
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
        "absolute bg-cultured text-prussianBlue w-1/3 max-h-[66%] overflow-auto top-20 right-6 z-10 pt-2 pb-2 text-left rounded-3xl shadow-md animate-growDown origin-top-right inline-block text-xl font-display " +
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

      <Link
        to="/dashboard-mentee"
        className="flex flex-row hover:font-semibold pr-6 pl-6 pb-4 pt-4 border-b-[1px] border-gray-300"
      >
        <BiCog className="text-2xl m-auto ml-0 mr-2" />
        <h2>Settings</h2>
      </Link>

      <Link
        to="/"
        className="flex flex-row hover:font-semibold pr-6 pl-6 pb-4 pt-4"
      >
        <BiLogOut className="text-2xl m-auto ml-0 mr-2" />
        <h2>Log out</h2>
      </Link>
    </div>
  );
};

export default UserMenu;

import React from "react";
import "./App.css";
import axios from "axios";
import NavBar from "./components/NavBar";
import PlanOfAction from "./components/PlanOfAction";
import MentorDetails from "./components/MentorDetails";
import Meeting from "./components/Meeting";

function DashboardMentee() {
  const dummyDate0 = new Date("2022-02-25");
  const dummyDate1 = new Date("2022-02-04");
  const dummyDate2 = new Date("2022-01-27");
  const dummyDate3 = new Date("2022-01-24");

  const dummyText1 =
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In ornare in ut iaculis sapien, id orci, pulvinar dui. Dui pulvinar eget varius et, et elit vitae, blandit. Nam in risus laoreet tellus. Pellentesque id ultrices rhoncus viverra nullam pretium tristique quam. Nibh felis posuere in non lectus est. Quis nullam porta sed pellentesque dui. Sed phasellus in vitae mi amet enim blandit. Eu neque viverra aenean porta cras.";
  const dummyText2 =
    "Aliquam rhoncus, faucibus imperdiet elementum. Ac praesent condimentum massa nam eu. Duis tellus aenean nunc id interdum. Mattis imperdiet fringilla purus tortor, egestas interdum. Eget posuere vel semper maecenas aliquet vulputate mattis aliquet.";
  const dummyText3 =
    "Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?";

  return (
    // <div className="fixed h-full w-full overflow-scroll overflow-x-auto">
    <div className="fixed h-full w-full">
      <NavBar activeStr="My mentors" />

      {/* Main flexbox */}
      <div className="flex flex-row items-stretch h-full font-display">
        {/* White half */}
        <div className="bg-cultured h-full w-2/3 m-auto flex text-prussianBlue fixed left-0 overflow-auto">
          <div className="flex flex-col w-[100%]">
            <MentorDetails
              firstName="John"
              lastName="Doe"
              topic="Random topic"
              nextMeeting={dummyDate0}
            />

            <div className="w-[90%] flex flex-col mr-auto ml-auto pb-44">
              <Meeting date={dummyDate1} feedback={dummyText1.repeat(2)} />
              <Meeting date={dummyDate2} feedback={dummyText2.repeat(3)} />
              <Meeting date={dummyDate3} feedback={dummyText3.repeat(4)} />
            </div>
          </div>
        </div>

        <PlanOfAction />
      </div>
    </div>
  );
}

export default DashboardMentee;

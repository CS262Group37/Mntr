import React from "react";

function LeftPanel() {
  return (
    // Blue half (login + registration page)
    <div className="flex h-full bg-blueBg bg-cover w-2/5 flex-col text-left">
      <h1 className="mt-40 ml-[12%] mr-[20%] text-cultured font-bold text-8xl leading-tight">Website Name</h1>
      <div className="ml-[12%] mb-28 mt-auto text-imperialRed text-5xl">
        <ul className="flex flex-col content-between space-y-5">
          <li>
            LEARN
          </li>
          <li>
            TEACH
          </li>
          <li>
            EXPERIENCE
          </li>
        </ul>
      </div>
    </div>
  );
}

export default LeftPanel;
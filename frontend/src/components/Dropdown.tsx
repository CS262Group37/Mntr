import React from "react";

interface DropdwonProps {
  onChange: any,
  values: string[],
  labels: string[],
  icon: JSX.Element
}

const Dropdown = (props:DropdwonProps) => {

  return (
    <div className="flex flex-row bg-cultured text-2xl text-prussianBlue w-full border-b-2 border-imperialRed">
      {props.icon}
      <select
        className="form-select appearance-none
        block
        w-full
        px-3
        py-1.5
        font-normal
        bg-cultured bg-clip-padding bg-no-repeat
        text-2xl
        rounded
        transition
        ease-in-out
        m-0
        focus:outline-none focus:bg-cultured"
        onChange={props.onChange}
      >
        
       {props.values.map((value, i) => (
         <option className="bg-cultured hover:bg-cultured" key={i} value={value}>{props.labels[i]}</option>
       ))}
      </select>
    </div>
  );
}

export default Dropdown;
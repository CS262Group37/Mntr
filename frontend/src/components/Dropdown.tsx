import React from "react";

interface DropdwonProps {
  onChange: any,
  placeholder: string
  values: string[],
  icon: JSX.Element
}

const Dropdown = (props:DropdwonProps) => {

  return (
    <div className="flex flex-row bg-cultured text-2xl text-prussianBlue w-full border-b-2 border-imperialRed">
      {props.icon}
      <select
        className="bg-cultured text-2xl p-4 pl-3 text-prussianBlue w-full form-select border-none rounded appearance-none focus:border-none "
        onChange={props.onChange}
      >
        <option className="bg-cultured text" value="" disabled selected hidden>{props.placeholder}</option>
       {props.values.map(value => (
         <option className="bg-cultured" value={value}>{value}</option>
       ))}
      </select>
    </div>
  );
}

export default Dropdown;
import React from "react";

interface TextInputProps {
  type: string,
  value: string,
  onChange: any,
  placeholder: string,
  icon: JSX.Element
}

const TextInput: React.FC<TextInputProps> = (props) => {
  return (
    <div className="flex flex-row bg-cultured text-2xl text-prussianBlue w-full border-b-2 border-imperialRed">
      {props.icon}
      <input
        className="bg-cultured bg-opacity-0 text-2xl p-4 pl-3 text-prussianBlue w-full focus:outline-none"
        type={props.type}
        value={props.value}
        onChange={props.onChange}
        placeholder={props.placeholder}
      />
    </div>
  );
}

export default TextInput;
import React from "react";

const TextInput = (props:any) => {
  const {
    type,
    value,
    onChange,
    placeholder,
    icon
  } = props;

  return (
    <div className="flex flex-row bg-cultured text-2xl text-prussianBlue w-full border-b-2 border-imperialRed">
      {icon}
      <input
        className="bg-cultured bg-opacity-0 text-2xl p-4 pl-3 text-prussianBlue w-full focus:outline-none"
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
      />
    </div>
  );
}

export default TextInput;
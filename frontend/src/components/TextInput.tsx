import { TextField } from "@mui/material";
import React from "react";

interface TextInputProps {
  type: string;
  value: string;
  onChange: any;
  placeholder: string;
  icon: JSX.Element;
}

const TextInput: React.FC<TextInputProps> = (props) => {
  return (
    // <div className="flex flex-row bg-cultured text-2xl text-prussianBlue w-full border-b-2 border-imperialRed focus:border-imperialRed focus-within:border-b-4 rou mb-[2px] focus-within:mb-0 box-border">
    //   {props.icon}
    //   <div className="relative group w-[100%]">
    //     <input
    //       required
    //       id={props.placeholder}
    //       className="bg-cultured bg-opacity-0 text-2xl p-4 pl-3 text-prussianBlue w-full outline-none peer"
    //       type={props.type}
    //       value={props.value}
    //       onChange={props.onChange}
    //       // placeholder={props.placeholder}
    //     />
    //     <label htmlFor={props.placeholder} className="transform absolute top-0 left-0 transition-all h-full flex items-center pl-3 text-2xl group-focus-within:text-xs group-focus-within:-translate-y-full group-focus-within:h-1/4 peer-valid:text-xs peer-valid:h-1/4 peer-valid:-translate-y-full">{props.placeholder}</label>
    //   </div>
    // </div>
    <TextField
      required
      id={props.placeholder}
      label={props.placeholder}
      variant="standard"
      type={props.type}
      onChange={props.onChange}
      InputProps={
        {
          startAdornment: props.icon
        }
      }
      sx={{
        input: {
          color: "#0E2A47",
          fontFamily: "Nunito",
          fontSize: 20,
          padding: 2,
          marginTop: 2,
          paddingLeft: 0,
        },
        label: {
          color: "#0E2A47",
          fontFamily: "Nunito",
          fontSize: 20,
          padding: 2,
          paddingLeft: 1,
        },
      }}
      fullWidth
    />
  );
};

export default TextInput;

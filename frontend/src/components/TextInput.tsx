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

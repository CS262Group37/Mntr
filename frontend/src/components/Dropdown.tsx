import { autocompleteClasses, InputLabel, ListItemIcon, MenuItem, Select } from "@mui/material";

interface DropdwonProps {
  onChange: any;
  values: string[];
  labels: string[];
  mainLabel: string;
  defaultVal?: string;
  icon: JSX.Element;
}

const Dropdown = (props: DropdwonProps) => {
  return (
    // <div className="flex flex-row bg-cultured text-2xl text-prussianBlue w-full border-b-2 border-imperialRed focus-within:border-b-4">
    //   {props.icon}
    //   <select
    //     className="form-select appearance-none
    //     block
    //     w-full
    //     px-3
    //     py-1.5
    //     font-normal
    //     bg-cultured bg-clip-padding bg-no-repeat
    //     text-2xl
    //     rounded
    //     transition
    //     ease-in-out
    //     m-0
    //     focus:outline-none focus:bg-cultured"
    //     onChange={props.onChange}
    //   >

    //    {props.values.map((value, i) => (
    //      <option className="bg-cultured hover:bg-cultured" key={i} value={value}>{props.labels[i]}</option>
    //    ))}
    //   </select>
    // </div>

    <>
      {/* <InputLabel id={props.mainLabel}>{props.mainLabel}</InputLabel> */}
      <Select
        labelId={props.mainLabel}
        label={props.mainLabel}
        id="demo-simple-select"
        onChange={props.onChange}
        value={props.defaultVal}
        sx={{
          color: "#0E2A47",
          fontFamily: "Nunito",
          fontSize: 20,
          padding: 1,
          paddingLeft: 0,
          textAlign: "left",
          // '& .ChildSelector': {
          //   bgcolor: 'cultured',
          // },
        }}
      >
        {props.values.map((v, i) => {
          return (
            <MenuItem value={v}>
              <div className="flex flex-row">
                <ListItemIcon>{props.icon}</ListItemIcon>
                <h1 className="m-auto ml-0">{props.labels[i]}</h1>
              </div>
            </MenuItem>
          );
        })}
        {/* <MenuItem value={10}>Ten</MenuItem>
      <MenuItem value={20}>Twenty</MenuItem>
      <MenuItem value={30}>Thirty</MenuItem> */}
      </Select>
    </>
  );
};

export default Dropdown;

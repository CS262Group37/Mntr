import { ListItemIcon, MenuItem, Select } from "@mui/material";

interface DropdwonProps {
  onChange: any;
  values: string[];
  labels: string[];
  mainLabel: string;
  defaultVal: string;
  icon: JSX.Element;
}

const Dropdown = (props: DropdwonProps) => {
  return (
    <>
      {/* <InputLabel id={props.mainLabel}>{props.mainLabel}</InputLabel> */}
      <Select
        required
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

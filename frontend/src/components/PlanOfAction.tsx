import React, { useEffect } from "react";
import Checkbox from "@mui/material/Checkbox";
import FormControlLabel from "@mui/material/FormControlLabel";
import axios from "axios";
import { BiPlus } from "react-icons/bi";
import {
  Avatar,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  TextField,
  Tooltip,
} from "@mui/material";

// TODO add a goal to the plan of action

interface PlanProps {
  goals: Goal[];
  relationID: number;
  handleNewGoal: () => void;
}

interface Goal {
  goalID?: number;
  title: string;
  description: string;
  creationDate?: Date;
  status: string;
}

interface ListElemProps {
  goal: Goal;
}

const ListElem: React.FC<ListElemProps> = (props) => {
  // TODO add onChange functionality
  const goal: Goal = props.goal;
  let isChecked: boolean = false;

  if (goal.status === "complete") isChecked = true;

  const [checked, setChecked] = React.useState(isChecked);

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (checked)
      axios.put("/api/plan/mark-plan-incomplete", { planID: goal.goalID });
    else axios.put("/api/plan/mark-plan-complete", { planID: goal.goalID });

    setChecked(event.target.checked);
  };

  return (
    <Tooltip followCursor title={<h1 className="text-[14px] font-thin ">{goal.description}</h1>}>
    <div className="text-prussianBlue bg-cultured shadow-md w-[82%] rounded-lg m-auto mt-3 mb-3 opacity-80 p-1 pr-4 pl-4 hover:opacity-90 transition duration-150">
      <FormControlLabel
        className="w-[100%]"
        value="end"
        control={
          <Checkbox
            className="text-cultured font-body"
            checked={checked}
            onChange={handleChange}
            sx={{
              "& .MuiSvgIcon-root": { fontSize: 28 },
              color: "#0E2A47",
              "&.Mui-checked": {
                color: "#0E2A47",
              },
            }}
          />
        }
        label={goal.title}
        labelPlacement="end"
      />
    </div>
    </Tooltip>
  );
};

// TODO fix ordering (complete first, incomplete first?)
const PlanOfAction: React.FC<PlanProps> = (props) => {
  const [open, setOpen] = React.useState(false); // dialog open/closed
  const [title, setTitle] = React.useState<string>("");
  const [desc, setDesc] = React.useState<string>("");

  const addGoal = () => {
    console.log(title + " " + desc);
    axios.post("/api/plan/add-plan", { relationID: props.relationID, title: title, description: desc }).then(() => {
      props.handleNewGoal();
    });
    setOpen(false);
    
  };

  return (
    <div className="flex h-full bg-blueBg bg-cover w-1/3 flex-col text-left fixed right-0 text-cultured overflow-auto pb-44">
      <div className="flex flex-row justify-between mt-2">
        <h1 className="text-3xl font-semibold m-10 ml-12 mr-12 mb-8">
          Plan of action
        </h1>

        <button
          className="bg-firebrick text-cultured text-xl p-2 m-auto mr-10 ml-5 rounded-full shadow-md transition ease-in-out hover:bg-imperialRed duration-200"
          onClick={() => setOpen(true)}
        >
          <BiPlus className="h-10 w-10 p-2" />
        </button>

        <Dialog onClose={() => setOpen(false)} open={open} fullWidth={true}>
          <DialogTitle>Add a goal</DialogTitle>
          <DialogContent>
            <div className="flex flex-col space-y-3">
              <TextField
                label="Title"
                onChange={(e: any) => {
                  setTitle(e.target.value);
                }}
              ></TextField>
              <TextField
                label="Description"
                multiline
                onChange={(e: any) => {
                  setDesc(e.target.value);
                }}
              ></TextField>
            </div>
          </DialogContent>
          <DialogActions>
            <Button onClick={addGoal} sx={{ color: "#0E2A47" }}>
              Add goal
            </Button>
          </DialogActions>
        </Dialog>
      </div>

      <div className="flex flex-col">
        {props.goals.map((goal: Goal) => {
          // console.log(meeting);
          return <ListElem goal={goal} />;
        })}
      </div>
    </div>
  );
};

export default PlanOfAction;

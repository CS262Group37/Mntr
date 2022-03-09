import React, { useEffect } from "react";
import Checkbox from "@mui/material/Checkbox";
import FormControlLabel from "@mui/material/FormControlLabel";
import axios from "axios";

// TODO add a goal to the plan of action

interface PlanProps {
  goals: Goal[];
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

  if (goal.status === "complete")
    isChecked = true;

  const [checked, setChecked] = React.useState(isChecked);

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setChecked(event.target.checked);
    // if (goal.status === "complete")
    //   goal.status = "incomplete";
    // else
    //   goal.status = "complete";
  };


  return (
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
  );
};

const PlanOfAction: React.FC<PlanProps> = (props) => {
  // const [goals, setGoals] = React.useState<Goal[]>([]);

  // useEffect(() => {
  //   let newGoals: Goal[];

  //   axios
  //     .get("/api/plan/get-plan", { params: { relationID: props.relationID } })
  //     .then((res: any) => {
  //       newGoals = res.data.map((g:any) => {
  //         return {
  //           goalID: g.goalid,
  //           title: g.title,
  //           description: g.description,
  //           // creationDate?: Date;
  //           status: g.status,
  //         }
  //       });
  //       console.log(newGoals);  

  //       // dummy data
  //       setGoals([
  //         {title: "goal 1", description: "just another goal", status: "complete"},
  //         {title: "goal 2", description: "just another goal", status: "complete"},
  //         {title: "goal 3", description: "just another goal", status: "incomplete"},
  //         {title: "goal 4", description: "just another goal", status: "incomplete"},
  //         {title: "goal 5", description: "just another goal", status: "incomplete"},
  //       ]);

  //       setGoals(newGoals);
  //     });
  // }, []);

  return (
    <div className="flex h-full bg-blueBg bg-cover w-1/3 flex-col text-left fixed right-0 text-cultured">
      <h1 className="text-3xl font-semibold m-10 ml-12 mr-12 mb-8">
        Plan of action
      </h1>

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

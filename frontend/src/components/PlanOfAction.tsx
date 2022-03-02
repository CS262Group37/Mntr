import React from "react";
import Checkbox from "@mui/material/Checkbox";
import FormControlLabel from "@mui/material/FormControlLabel";

const ListElem = (props: any) => {
  // TODO add onChange functionality
  const { label } = props;

  return (
    <div className="text-prussianBlue bg-cultured shadow-md w-[82%] rounded-lg m-auto mt-3 mb-3 opacity-80 p-1 pr-4 pl-4">
      <FormControlLabel
        className="w-[100%]"
        value="end"
        control={
          <Checkbox
            className="text-cultured font-body"
            sx={{
              "& .MuiSvgIcon-root": { fontSize: 28 },
              color: "#0E2A47",
              "&.Mui-checked": {
                color: "#0E2A47",
              },
            }}
          />
        }
        label={label}
        labelPlacement="end"
      />
    </div>
  );
};

function PlanOfAction() {
  const goals: string[] = ["goal1", "goal2", "goal3", "goal4", "goal5", "goal6"];

  const listItems = goals.map((label) => {
    return <ListElem label={label} />;
  })

  return (
    <div className="flex h-full bg-blueBg bg-cover w-1/3 flex-col text-left fixed right-0 text-cultured">
      <h1 className="text-3xl font-semibold m-10 ml-12 mr-12 mb-8">
        Plan of action
      </h1>

      <div className="flex flex-col">
        {listItems}
      </div>
    </div>
  );
}

export default PlanOfAction;

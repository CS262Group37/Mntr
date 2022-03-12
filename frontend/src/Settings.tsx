import { Divider, TextField, Tooltip } from "@mui/material";
import axios from "axios";
import { useEffect, useState } from "react";
import { BiCommentAdd } from "react-icons/bi";
import NavBarMentee from "./components/NavBarMentee";
import NavBarMentor from "./components/NavBarMentor";

function Settings() {
  const [loggedInRole, setLoggedInRole] = useState<string>("");
  const [feedback, setFeedback] = useState<string>("");
  const [newPasswd, setNewPasswd] = useState<string>("");
  const [newPasswdConf, setNewPasswdConf] = useState<string>("");

  useEffect(() => {
    axios.get("/api/users/get-own-data").then((res) => {
      setLoggedInRole(res.data.role);
    });
  }, []);

  // TODO
  const changePassword = () => {};

  const submitFeedback = () => {
    axios
      .put("/api/admin/create-app-feedback", { content: feedback })
      .then((res) => {
        console.log(res);
        alert("Thank you for your feedback!");
      });
  };

  return (
    <div className="fixed h-full w-full">
      {loggedInRole === "mentee" && <NavBarMentee activeStr="Settings" />}
      {loggedInRole === "mentor" && <NavBarMentor activeStr="Settings" />}

      {/* Main flexbox */}
      <div className="h-full w-full font-display bg-cultured overflow-auto p-6 flex flex-col pb-40">
        {/* App feedback */}
        <div className="flex flex-col bg-gray-300 bg-opacity-50 shadow-md m-auto mt-5 mb-5 w-[70%] text-prussianBlue p-4 rounded-xl text-left">
          {/* Account settings */}
          <h1 className="text-3xl m-4 text-firebrick">Account settings</h1>
          <Divider />
          <h2 className="m-4 mb-2 text-lg font-semibold">Change password:</h2>
          <div className="m-4 mt-0 flex flex-col space-y-3">
            {/* New password */}
            <TextField
              placeholder="Enter new password"
              value={newPasswd}
              onChange={(e: any) => setNewPasswd(e.target.value)}
              size="small"
              sx={{
                width: "30%",
                textarea: {
                  color: "#0E2A47",
                },
              }}
            ></TextField>

            {/* Confirm password */}
            <TextField
              placeholder="Confirm new password"
              value={newPasswdConf}
              onChange={(e: any) => setNewPasswdConf(e.target.value)}
              size="small"
              sx={{
                width: "30%",
                textarea: {
                  color: "#0E2A47",
                },
              }}
            ></TextField>

            <Tooltip title="Submit changes" arrow>
              <button
                className="bg-prussianBlue text-cultured text-lg p-2 pl-4 pr-4 m-auto rounded-full shadow-md transition ease-in-out hover:bg-brightNavyBlue duration-200 ml-0"
                onClick={changePassword}
              >
                Submit changes
              </button>
            </Tooltip>
          </div>
        </div>

        {/* App feedback */}
        <div className="flex flex-col bg-gray-300 bg-opacity-50 shadow-md m-auto mt-5 mb-5 w-[70%] text-prussianBlue p-4 rounded-xl text-left">
          <h1 className="text-3xl m-4 text-firebrick">Submit app feedback</h1>
          <Divider />
          <p className="m-4 text-lg">
            If you have any suggestions, issues or any other enquiries, please
            enter them below. Thank you for using{" "}
            <span className="text-firebrick font-bold">Mntr</span>!
          </p>
          <div className="m-4 mt-0 flex flex-row space-x-5">
            <TextField
              value={feedback}
              onChange={(e: any) => setFeedback(e.target.value)}
              multiline
              fullWidth
              sx={{
                textarea: {
                  color: "#0E2A47",
                },
              }}
            ></TextField>
            <Tooltip title="Submit feedback" arrow>
              <button
                className="bg-prussianBlue text-cultured text-xl p-3 m-auto rounded-full shadow-md transition ease-in-out hover:bg-brightNavyBlue duration-200 mr-0"
                onClick={submitFeedback}
              >
                <BiCommentAdd className="h-8 w-8 p-1" />
              </button>
            </Tooltip>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Settings;

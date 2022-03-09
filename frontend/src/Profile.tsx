import React, { useEffect } from "react";
import axios from "axios";
import { BiEnvelope, BiMenu, BiMenuAltRight, BiUserCircle } from "react-icons/bi";
import { Link, useLocation } from "react-router-dom";
import { Avatar, Popover, Rating, Typography } from "@mui/material";
import NavBar from "./components/NavBarMentee";

interface UserData {
  id?: number;
  email: string;
  firstName: string;
  lastName: string;
  avatar: string;
  role: string;
  businessArea: string;
  topics?: string[];
  ratings?: Rating[];
}

interface Rating {
  skill: string;
  rating: number;
}

function useQuery() {
  const { search } = useLocation();

  return React.useMemo(() => new URLSearchParams(search), [search]);
}

function Profile() {
  const [user, setUser] = React.useState<UserData>({
    email: "",
    firstName: "",
    lastName: "",
    avatar: "",
    role: "",
    businessArea: "",
  });
  const [mentor, setMentor] = React.useState<UserData[]>([]);

  let query = useQuery();
  const userIdQuery = query.get("id");
  let userID: number = -1;

  if (userIdQuery != null) userID = parseInt(userIdQuery);

  useEffect(() => {
    // Get user data
    axios
      .post("/api/users/get-user-data", { userID: userID })
      .then(async (res) => {
        console.log(res.data);
        var newTopics: string[] = [];
        var newRatings: Rating[] = [];
        const newUser = {
          email: res.data.email,
          firstName: res.data.firstname,
          lastName: res.data.lastname,
          avatar: res.data.profilepicture,
          role: res.data.role,
          businessArea: res.data.businessarea,
        };

        // Get topics
        await axios
          .post("/api/users/get-user-topics", { userID: userID })
          .then((res) => {
            const arr: string[] = [];
            res.data.map((t: any) => {
              arr.push(t.topic);
            });

            newTopics = arr;
          });

        // Get ratings
        if (newUser.role === "mentor") {
          await axios
            .post("/api/users/get-user-ratings", { userID: userID })
            .then((res) => {
              // Sort alphabetically by skill
              res.data.sort((e1: any, e2: any) => {
                return e2.skill < e1.skill;
              });

              newRatings = res.data;
            });
        }
        setUser({
          id: userID,
          email: newUser.email,
          firstName: newUser.firstName,
          lastName: newUser.lastName,
          avatar: newUser.avatar,
          role: newUser.role,
          businessArea: newUser.businessArea,
          topics: newTopics,
          ratings: newRatings,
        });
      });
  }, []);

  // TODO connect to a mentor function
  const connectMentor = () => {
    return;
  };

  return (
    <div className="fixed h-full w-full">
      <NavBar activeStr="Public profile" setMentor={setMentor}/>

      {/* Main flexbox */}
      <div className="h-full w-full font-display  bg-cultured overflow-auto p-6 flex flex-col pb-40">
          <div className="flex flex-col bg-gray-300 bg-opacity-50 shadow-md m-auto mt-5 mb-5 w-[70%] text-prussianBlue p-8 rounded-xl text-left">
          <div className="flex flex-row mb-6 justify-between">
            <Avatar
              className="m-2"
              alt={user.firstName + " " + user.lastName}
              src={user.avatar}
              sx={{ width: 140, height: 140 }}
            />
            {/* Mentor name & topics */}
            <div className="flex flex-col text-left m-auto ml-0 pl-4 space-y-3 text-firebrick">
              <h2 className="font-semibold text-4xl">
                {user.firstName + " " + user.lastName}
              </h2>

              <h3 className="text-xl">{user.role.toUpperCase()}</h3>
            </div>
            
            <button
              className="bg-firebrick text-cultured text-xl min-w-80 p-4 m-auto mt-2 mr-2 ml-5 rounded-full shadow-md transition ease-in-out hover:bg-imperialRed duration-200"
              onClick={connectMentor}
            >
              <BiEnvelope className="h-12 w-12 p-2" />
            </button>
          </div>

          {/* Topics and business area */}
          <div className="text-lg m-4 mt-2">
            <p className="text-xl mb-2">
              <span className="font-bold">TOPICS: </span>
              {user.topics?.map((topic, i, { length }) => {
                if (i === length - 1) {
                  return <span>{topic}</span>;
                } else return <span>{topic + ", "}</span>;
              })}
            </p>
            <p><span className="font-bold">BUSINESS AREA:</span> {user.businessArea}</p>
          </div>

          {/* Bio */}
          <div className="bg-cultured rounded-lg p-4 pb-2 font-body m-4">
            <div className="flex flex-row text-2xl border-b-2 border-imperialRed justify-between">
              <h1 className="font-bold mt-1 mb-3 ml-3 text-left font-display text-xl">
                BIO
              </h1>
            </div>

            <div className="mb-3 ml-3 mt-4 text-justify space-y-1">
              <p>My name is {user.firstName}.</p>
              <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. In ornare in ut iaculis sapien, id orci, pulvinar dui. Dui pulvinar eget varius et, et elit vitae, blandit. Nam in risus laoreet tellus. Pellentesque id ultrices rhoncus viverra nullam pretium tristique quam.</p>
              <p>Mattis imperdiet fringilla purus tortor, egestas interdum. Eget posuere vel semper maecenas aliquet vulputate mattis aliquet.</p>
              <p>Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?</p>
            </div>
          </div>

          {/* Ratings */}
          <div className="flex flex-row justify-evenly overflow-clip flex-wrap mt-4">
            {user.ratings?.map((rating) => {
              return (
                <div className="p-1">
                  <Typography component="legend">{rating.skill}</Typography>
                  <Rating name="read-only" value={rating.rating} readOnly />
                </div>
              );
            })}
          </div>
        </div>
        {/* {user.firstName + " " + user.lastName} */}
      </div>
    </div>
  );
}

export default Profile;

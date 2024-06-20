import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
// import APIService from "../services/APIService";

const UserProfile = () => {
  const [username, setUsername] = useState<string>("");
  const [motto, setMotto] = useState<string>("");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUser = async () => {
      const response = await fetch("http://localhost:3002/user", {
        credentials: "include",
      });
      const data = await response.json();
      if (response.ok) {
        setUsername(data.username);
        setMotto(data.motto);
      } else {
        navigate("/login");
      }
    };
    fetchUser();
  }, [navigate]);

  const handleLogout = () => {
    document.cookie = "token=; Max-Age=0; path=/";
    navigate("/login");
  };

  return (
    <div className="container">
      <img src="" />
      <div className="user">{username}</div>

      <div className="user-motto">{motto}</div>
      <div className="button-area">
        <button>Record (New) Audio</button>
        <button onClick={handleLogout}>Logout</button>
      </div>
    </div>
  );
};

export default UserProfile;

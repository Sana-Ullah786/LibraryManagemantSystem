import React, { useContext } from "react";
import { AuthContext } from "../../contexts/AuthContext";

// After a successful API call, the data element should be populated as HomeData type
export type HomeData = {
  num_authors: number;
  num_books: number;
  num_fantasy_genres: number;
  num_instances: number;
  num_instances_available: number;
  num_lotr_books: number;
};

function Home() {
  /**
   * This displays the aggregate data needed to be displayed on the home page.
   * It collects this data using the API endpoint for the home page.
   * This home page is a custom API view on the Django app.
   * The behavior in case the API call fails has not been implemented yet.
   * The original Django app also had a counter to keep track of the number of times
   * the home page was visited. This has not been implemented yet either.
   */
  // The state of the component is used to store the JSON data received from the API endpoint
  const { username }: { username: string } = useContext(AuthContext);

  return (
    <div
      className="background-image"
    >
      <h1>Welcome {username}</h1>
    </div>
  );
}

export default Home;

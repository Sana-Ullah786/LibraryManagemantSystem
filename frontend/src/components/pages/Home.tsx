import React, { useContext } from "react";
import { AuthContext } from "../../contexts/AuthContext";

//After a successful api call, the data element should be populated as HomeData type
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
   * This displays the agregate data needed to be displayed at the home page
   * It collects this data using the API end point for the home page.
   * This home page is a custom api view on the django app.
   * The behaviour in case the api call fails has not been implemented yet.
   * The original Django app also had a counter to keep track of the number of times
   * the home page was visited. This has not been implemented yet either.
   */
  //The state of the component is used to store the JSON data recieved fromt the api end point
  const { username }: { username: string } = useContext(AuthContext);

  return(

    <div style={{justifyItems:'center'}}>
      <h1>Welcome {username}</h1>
    </div>

  )
}

export default Home;

import React from 'react';
import { Link } from 'react-router-dom';
import { UserDetails } from '../../CustomTypes';


export type UserListItemProps = {
    key: number;
    item: UserDetails;
    linksto: string;
  };
  

function UserListItem({ item, linksto }: UserListItemProps) {
  return (
    <div className='modal'>
      <h2>{item.username}</h2>
      <p>Email: {item.email}</p>
      <Link to={linksto}>View Details</Link><br/>
      <Link to={`/users/${item.id}/update`}>Update</Link>  
    </div>
  );
}

export default UserListItem;

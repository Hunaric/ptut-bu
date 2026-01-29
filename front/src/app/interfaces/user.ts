// user.model.ts

import { Account } from "./account";
import { Permission } from "./permission";
import { Role } from "./role";

export interface User {
  id: string;           // UUID
  email: string;
  username: string;
  first_name?: string;
  last_name?: string;
  is_active: boolean;
  role?: Role;
  permissions?: Permission[];
  account?: Account;
}

export interface Me {
  id: string;             // UUID
  username: string;           // UUID
  email: string;
  role?: Role;
  permissions?: Permission[];
}

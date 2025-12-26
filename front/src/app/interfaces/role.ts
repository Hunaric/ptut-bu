// role.model.ts

import { Permission } from "./permission";

export interface Role {
  id: number;
  name: string;          // student, admin, teacher
  description?: string;
  permissions?: Permission[];
}

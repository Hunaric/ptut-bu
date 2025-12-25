// role.model.ts
import { Permission } from './permission.model';

export interface Role {
  id: number;
  name: string;          // student, admin, teacher
  description?: string;
  permissions?: Permission[];
}

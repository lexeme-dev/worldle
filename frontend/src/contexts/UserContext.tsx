import { useMutation, useQuery } from "@tanstack/react-query";
import React, { createContext, useContext } from "react";
import { DefaultService } from "../client";

const USER_UUID_KEY = "worldle_user_uuid";

interface UserContext {
  uuid: string | undefined;
  isLoading: boolean;
}

const UserContext = createContext<UserContext | null>(null);

export const UserProvider: React.FC<{
  children: React.ReactNode;
}> = ({ children }) => {
  const createUserClient = useMutation({
    mutationFn: async () => {
      const { data } = await DefaultService.createUserClient();
      localStorage.setItem(USER_UUID_KEY, data.uuid);
      return data.uuid;
    },
  });

  const { data: uuid, isLoading } = useQuery({
    queryKey: ["user"],
    queryFn: async () => {
      const storedUuid = localStorage.getItem(USER_UUID_KEY);
      if (!storedUuid) {
        return createUserClient.mutateAsync();
      }

      try {
        // Verify the stored UUID is valid
        const { data: userClient } = await DefaultService.readUserClient({
          path: { user_client_uuid: storedUuid },
        });
        return userClient.uuid;
      } catch (error) {
        // If the UUID is invalid, create a new one
        localStorage.removeItem(USER_UUID_KEY);
        return createUserClient.mutateAsync();
      }
    },
  });

  return (
    <UserContext.Provider value={{ uuid, isLoading }}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = () => {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error("useUser must be used within a UserProvider");
  }
  return context;
};

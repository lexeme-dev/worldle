import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import React, { createContext, useContext } from "react";
import { DefaultService } from "../client";
import { readUserStatsOptions } from "../client/@tanstack/react-query.gen";

const USER_UUID_KEY = "worldle_user_uuid";

interface UserContext {
  uuid: string | undefined;
  isLoading: boolean;
  changeUserId: (newUuid: string) => Promise<void>;
  validateUserId: (uuid: string) => Promise<boolean>;
}

const UserContext = createContext<UserContext | null>(null);

export const UserProvider: React.FC<{
  children: React.ReactNode;
}> = ({ children }) => {
  const queryClient = useQueryClient();

  const createUserClient = useMutation({
    mutationFn: async () => {
      const { data } = await DefaultService.createUserClient();
      localStorage.setItem(USER_UUID_KEY, data.uuid);
      return data.uuid;
    },
  });

  const changeUserIdMutation = useMutation({
    mutationFn: async (newUuid: string) => {
      // Verify the UUID exists
      await DefaultService.readUserClient({
        path: { user_client_uuid: newUuid },
      });
      localStorage.setItem(USER_UUID_KEY, newUuid);
      await queryClient.invalidateQueries({ queryKey: ["user"] });
    },
  });

  const validateUserId = async (uuid: string): Promise<boolean> => {
    try {
      await DefaultService.readUserClient({
        path: { user_client_uuid: uuid },
      });
      return true;
    } catch {
      return false;
    }
  };

  const { data: uuid, isLoading } = useQuery({
    queryKey: ["user"],
    queryFn: async () => {
      const storedUuid = localStorage.getItem(USER_UUID_KEY);
      if (!storedUuid) {
        console.log("No user client found, creating one");
        return createUserClient.mutateAsync();
      }

      console.log("Verifying user client", storedUuid);
      const { data: userClient } = await DefaultService.readUserClient({
        path: { user_client_uuid: storedUuid },
      });
      if (userClient != null) {
        queryClient.prefetchQuery({
          ...readUserStatsOptions({
            path: { user_client_uuid: userClient.uuid },
          }),
          staleTime: 60000 * 5,
        });
      }
      return userClient.uuid;
    },
  });

  return (
    <UserContext.Provider
      value={{
        uuid,
        isLoading,
        changeUserId: changeUserIdMutation.mutateAsync,
        validateUserId,
      }}
    >
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

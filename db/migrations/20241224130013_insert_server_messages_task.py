from db.migration_manager import Migration

class InsertServerMessagesTask(Migration):
    id = 20241224130013

    def sql(self):
        return """
            INSERT INTO task (id, kind, interval, data)
            VALUES (
                1,
                'server_messages',
                180,
                '[
                    "Bem-vindo ao servidor KPX!\nLembre-se de seguir as regras e.\nrespeitar todos os jogadores.",
                    "Anti-Jogo >>> Denunciem no Discord <<<",
                    "Entre em nosso DISCORD: >>> bit.ly/GACKPX <<<",
                    "Regra 1: Respeite todos os jogadores, \nqualquer desrespeito será punido com ban permanente.",
                    "Regra 2: Comunique-se com o time, \ntrabalho em equipe é essencial.",
                    "Regra 4: Espere o time para capturar ou destruir\n o objetivo, na dúvida? Pergunte!",
                    "Regra 3: NÃO RUSHE NO OBJETIVO, ao morrer\n você prejudica o time, que terá de\n lidar com os bots que foram incluidos para você.",
                    "Regra 5: Evite Flashbang e Smoke, \nos bots conseguem ver através da fumaça e \nnão são tão afetados pela flash, acaba só \natrapalhando os colegas.",
                    "Rules: Respect all players. \nComunicate with your team. \nWait for the team to capture or destroy the objective. \nAvoid Flashbang and Smoke.",
                    "Regla: Respeta a todos los jugadores. \nComunícate con tu equipo. \nEspera a que el equipo capture o destruya el objetivo. \nEvita Flashbang y Smoke."
                ]'
            );
            """

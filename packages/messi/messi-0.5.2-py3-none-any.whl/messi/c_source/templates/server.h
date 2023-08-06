/*
 * The MIT License (MIT)
 *
 * Copyright (c) 2020, Erik Moqvist
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use, copy,
 * modify, merge, publish, distribute, sublicense, and/or sell copies
 * of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
 * BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
 * ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 *
 * This file is part of the Messi project.
 */

#ifndef {name_upper}_SERVER_H
#define {name_upper}_SERVER_H

#include <stdint.h>
#include "{name}_common.h"
#include "{name}.h"

struct {name}_server_t;
struct {name}_server_client_t;

{on_message_typedefs}
enum {name}_server_client_input_state_t {{
    {name}_server_client_input_state_header_t = 0,
    {name}_server_client_input_state_payload_t
}};

struct {name}_server_t {{
    const char *address_p;
{on_message_members}
    int epoll_fd;
    {name}_epoll_ctl_t epoll_ctl;
    int listener_fd;
    struct {name}_server_client_t *current_client_p;
    struct {{
        struct {name}_server_client_t *used_list_p;
        struct {name}_server_client_t *free_list_p;
        size_t input_buffer_size;
    }} clients;
    struct {{
        struct {name}_common_buffer_t data;
        size_t left;
    }} message;
    struct {{
        struct {name}_client_to_server_t *message_p;
        struct {name}_common_buffer_t workspace;
    }} input;
    struct {{
        struct {name}_server_to_client_t *message_p;
        struct {name}_common_buffer_t workspace;
    }} output;
}};

struct {name}_server_client_t {{
    int client_fd;
    int keep_alive_timer_fd;
    struct {{
        enum {name}_server_client_input_state_t state;
        uint8_t *buf_p;
        size_t size;
        size_t left;
    }} input;
    struct {name}_server_client_t *next_p;
    struct {name}_server_client_t *prev_p;
}};

/**
 * Initialize given server.
 */
int {name}_server_init(
    struct {name}_server_t *self_p,
    const char *address_p,
    struct {name}_server_client_t *clients_p,
    int clients_max,
    uint8_t *clients_input_bufs_p,
    size_t client_input_size,
    uint8_t *message_buf_p,
    size_t message_size,
    uint8_t *workspace_in_buf_p,
    size_t workspace_in_size,
    uint8_t *workspace_out_buf_p,
    size_t workspace_out_size,
{on_message_params}
    int epoll_fd,
    {name}_epoll_ctl_t epoll_ctl);

/**
 * Start serving clients.
 */
int {name}_server_start(struct {name}_server_t *self_p);

/**
 * Stop serving clients.
 */
void {name}_server_stop(struct {name}_server_t *self_p);

/**
 * Process any pending events on given file descriptor if it belongs
 * to given server.
 */
void {name}_server_process(struct {name}_server_t *self_p, int fd, uint32_t events);

/**
 * Send prepared message to given client.
 */
void {name}_server_send(struct {name}_server_t *self_p);

/**
 * Send prepared message to current client.
 */
void {name}_server_reply(struct {name}_server_t *self_p);

/**
 * Broadcast prepared message to all clients.
 */
void {name}_server_broadcast(struct {name}_server_t *self_p);

{init_messages}
#endif
